
from unittest.mock import MagicMock
from pytest import fixture

from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.account import Account, User
from src.domain.model.balance import Balance, BalanceType
from src.domain.model.transaction import TransactionRequest
from src.domain.service.authorizer import AuthorizationResult, TransactionsAuthorizer
from src.repository.mongodb import account as accounts_repository

class TestAuthorizerService:
    @fixture
    def service(self):
        return TransactionsAuthorizer()
    
    @fixture
    def repository(self):
           return accounts_repository
    
    @fixture
    def account(self):
        some_user = User(email='someone@gmail.com')
        balances=[
               Balance(type=BalanceType.FOOD),
               Balance(type=BalanceType.MEAL),
               Balance(type=BalanceType.CASH)
            ]
        return Account(user=some_user, balances=balances)   
    

    def test_should_not_authorized_transaction_not_enough_balance(self, account, service):
        service.accounts_service.get_account = MagicMock(return_value=account)
        service.accounts_service.debit = MagicMock(side_effect=NotEnoughBalanceException("error"))

        transaction_request = TransactionRequest(
            account_id=str(account.id),
            total_amount=23.90,
            mcc='1234',
            merchant='Padaria Silva'
        )

        result = service.authorize(transaction_request)

        assert result == AuthorizationResult.REJECTED_BALANCE

    def test_should_not_authorized_transaction_generic_error(self, account, service):
        service.accounts_service.get_account = MagicMock(return_value=account)
        service.accounts_service.debit = MagicMock(side_effect=Exception("generic error"))
        transaction_request = TransactionRequest(
            account_id=str(account.id),
            total_amount=23.90,
            mcc='1234',
            merchant='Padaria Silva'
        )

        result = service.authorize(transaction_request)

        assert result == AuthorizationResult.REJECTED_ERROR

    def test_should_authorized_transaction(self, account, service):
        service.accounts_service.get_account = MagicMock(return_value=account)
        
        service.accounts_service.debit = MagicMock()

        transaction_request = TransactionRequest(
            account_id=str(account.id),
            total_amount=23.90,
            mcc='1234',
            merchant='Padaria Silva'
        )
        
        result = service.authorize(transaction_request)

        assert result == AuthorizationResult.AUTHORIZED

    def test_should_authorized_cash_transaction(self, account, service, repository):
        repository.find_account = MagicMock(return_value=account)
        repository.update_balance = MagicMock(account)
        
        service.accounts_service.credit(account.id, BalanceType.CASH, 199.0)
        service.accounts_service.credit(account.id, BalanceType.FOOD, 300.0)
        
        assert account.get_balance(BalanceType.CASH).amount == 199.0

        transaction_request = TransactionRequest(
            account_id=str(account.id),
            total_amount=100.0,
            mcc='9999',
            merchant='Uber'
        )
        
        result = service.authorize(transaction_request)

        assert result == AuthorizationResult.AUTHORIZED
        assert account.get_balance(BalanceType.CASH).amount == 99.0
        assert account.get_balance(BalanceType.FOOD).amount == 300.0

    def test_should_authorized_meal_transaction(self, account, service, repository):
        repository.find_account = MagicMock(return_value=account)
        repository.update_balance = MagicMock(account)

        service.accounts_service.credit(account.id, BalanceType.CASH, 199.0)
        service.accounts_service.credit(account.id, BalanceType.FOOD, 300.0)
        service.accounts_service.credit(account.id,BalanceType.MEAL, 25.0)
        
        assert account.get_balance(BalanceType.MEAL).amount == 25.0

        transaction_request = TransactionRequest(
            account_id=str(account.id),
            total_amount=10.0,
            mcc='5812',
            merchant='Uau Pizza'
        )
        
        result = service.authorize(transaction_request)

        assert result == AuthorizationResult.AUTHORIZED
        assert account.get_balance(BalanceType.MEAL).amount == 15.0

    def test_should_authorized_food_transaction_but_debits_on_cash_balance(self, account, service, repository):
        repository.find_account = MagicMock(return_value=account)
        repository.update_balance = MagicMock(account)

        service.accounts_service.credit(account.id, BalanceType.CASH, 199.0)
        service.accounts_service.credit(account.id, BalanceType.FOOD, 2.0)

        assert account.get_balance(BalanceType.CASH).amount == 199.0
        assert account.get_balance(BalanceType.FOOD).amount == 2.00

        transaction_request = TransactionRequest(
            account_id=str(account.id),
            total_amount=10.0,
            mcc='5411',
            merchant='Uau Pizza'
        )

        result = service.authorize(transaction_request)

        assert result == AuthorizationResult.AUTHORIZED       
        assert account.get_balance(BalanceType.CASH).amount == 189.0
        assert account.get_balance(BalanceType.FOOD).amount == 2.00

    def test_should_extract_food_type(self, service):
        transaction_request = TransactionRequest(
            account_id='1234',
            total_amount=23.90,
            mcc='5811',
            merchant='Assai Atacad'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.FOOD


    def test_should_extract_meal_type(self, service):
        transaction_request = TransactionRequest(
            account_id='1234',
            total_amount=23.90,
            mcc='5411',
            merchant='Subway'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.MEAL

    def test_should_extract_cash_type(self, service):
        transaction_request = TransactionRequest(
            account_id='1234',
            total_amount=23.90,
            mcc='9999',
            merchant='V*G Padaria'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.CASH

    def test_should_extract_food_type(self, service):
        transaction_request = TransactionRequest(
            account_id='1234',
            total_amount=23.90,
            mcc='5411',
            merchant='V*G Padaria'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.FOOD