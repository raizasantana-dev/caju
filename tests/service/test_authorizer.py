
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
        some_user = User(123, 'someone@gmail.com')
        return Account(456, some_user)   
    

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
        
        current_balance = account.get_balance(BalanceType.FOOD)
        assert current_balance.amount == 300.0

        transaction_request = TransactionRequest(
            account.id,
            25.90,
            '5411',
            'Mercado Li'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED
        new_balance_food = account.get_balance(BalanceType.FOOD)
        assert new_balance_food.amount == 274.10

        new_balance_cash = account.get_balance(BalanceType.CASH)
        assert new_balance_cash.amount == 199.0

    def test_should_authorized_cash_transaction(self, account, service):
        account.credit(BalanceType.CASH, 199.0)
        account.credit(BalanceType.FOOD, 300.0)
        
        current_balance = account.get_balance(BalanceType.CASH)
        assert current_balance.amount == 199.0

        transaction_request = TransactionRequest(
            account.id,
            100.0,
            '9999',
            'Uber'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED
        new_balance_cash = account.get_balance(BalanceType.CASH)
        assert new_balance_cash.amount == 99.0

        new_balance_food = account.get_balance(BalanceType.FOOD)
        assert new_balance_food.amount == 300.0

    def test_should_authorized_meal_transaction(self, account, service):
        account.credit(BalanceType.CASH, 199.0)
        account.credit(BalanceType.FOOD, 300.0)
        account.credit(BalanceType.MEAL, 25.0)
        
        current_balance = account.get_balance(BalanceType.MEAL)
        assert current_balance.amount == 25.0

        transaction_request = TransactionRequest(
            account.id,
            10.0,
            '5812',
            'Uau Pizza'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.AUTHORIZED
        new_balance_cash = account.get_balance(BalanceType.MEAL)
        assert new_balance_cash.amount == 15.0

    