
from unittest.mock import MagicMock
from pytest import fixture

from src.domain.model.account import Account, User
from src.domain.model.balance import BalanceType
from src.domain.model.transaction import TransactionRequest
from src.domain.service.authorizer import AuthorizationResult, TransactionsAuthorizer


class TestAuthorizerService:
    @fixture
    def service(self):
        return TransactionsAuthorizer()
    
    @fixture
    def account(self):
        some_user = User(email='someone@gmail.com')
        return Account(user=some_user)   
    

    def test_should_not_authorized_transaction_not_enough_balance(self, account, service):
        assert account.get_balance(BalanceType.CASH).amount == 0.00

        transaction_request = TransactionRequest(
            account.id,
            23.90,
            '1234',
            'Padaria Silva'
        )

        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.REJECTED_BALANCE

    def test_should_not_authorized_transaction_generic_error(self, account, service):
        service.accounts_service.debit = MagicMock(side_effect=Exception("generic error"))
        transaction_request = TransactionRequest(
            account.id,
            23.90,
            '1234',
            'Padaria Silva'
        )

        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.REJECTED_ERROR

    def test_should_authorized_transaction(self, account, service):
        assert account.get_balance(BalanceType.CASH).amount == 0.00

        account.credit(BalanceType.CASH, 199.0)
        
        transaction_request = TransactionRequest(
            account.id,
            23.90,
            '1234',
            'Padaria Silva'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED


    def test_should_authorized_food_transaction(self, account, service):
        assert account.get_balance(BalanceType.CASH).amount == 0.00

        account.credit(BalanceType.CASH, 199.0)
        account.credit(BalanceType.FOOD, 300.0)
        
        assert account.get_balance(BalanceType.FOOD).amount == 300.0

        transaction_request = TransactionRequest(
            account.id,
            25.90,
            '5411',
            'Mercado Li'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED
        assert account.get_balance(BalanceType.FOOD).amount == 274.10
        assert account.get_balance(BalanceType.CASH).amount == 199.0

    def test_should_authorized_cash_transaction(self, account, service):
        account.credit(BalanceType.CASH, 199.0)
        account.credit(BalanceType.FOOD, 300.0)
        
        assert account.get_balance(BalanceType.CASH).amount == 199.0

        transaction_request = TransactionRequest(
            account.id,
            100.0,
            '9999',
            'Uber'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED
        assert account.get_balance(BalanceType.CASH).amount == 99.0
        assert account.get_balance(BalanceType.FOOD).amount == 300.0

    def test_should_authorized_meal_transaction(self, account, service):
        account.credit(BalanceType.CASH, 199.0)
        account.credit(BalanceType.FOOD, 300.0)
        account.credit(BalanceType.MEAL, 25.0)
        
        assert account.get_balance(BalanceType.MEAL).amount == 25.0

        transaction_request = TransactionRequest(
            account.id,
            10.0,
            '5812',
            'Uau Pizza'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED
        assert account.get_balance(BalanceType.MEAL).amount == 15.0

    def test_should_authorized_food_transaction_but_debits_on_cash_balance(self, account, service):
        account.credit(BalanceType.CASH, 199.0)
        account.credit(BalanceType.FOOD, 2.0)

        assert account.get_balance(BalanceType.CASH).amount == 199.0
        assert account.get_balance(BalanceType.FOOD).amount == 2.00

        transaction_request = TransactionRequest(
            account.id,
            10.0,
            '5411',
            'Uau Pizza'
        )

        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED       
        assert account.get_balance(BalanceType.CASH).amount == 189.0
        assert account.get_balance(BalanceType.FOOD).amount == 2.00

    def test_should_extract_food_type(self, service):
        transaction_request = TransactionRequest(
            1234,
            23.90,
            '5811',
            'Assai Atacad'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.FOOD


    def test_should_extract_meal_type(self, service):
        transaction_request = TransactionRequest(
            1234,
            23.90,
            '5411',
            'Subway'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.MEAL

    def test_should_extract_cash_type(self, service):
        transaction_request = TransactionRequest(
            1234,
            23.90,
            '9999',
            'V*G Padaria'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.CASH

    def test_should_extract_food_type(self, service):
        transaction_request = TransactionRequest(
            1234,
            23.90,
            '5411',
            'V*G Padaria'
        )

        result = service.extract_type(transaction_request)

        assert result == BalanceType.FOOD