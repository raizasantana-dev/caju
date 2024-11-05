
import pytest
from src.domain.model.account import Account, User
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import BalanceType


class TestAccountModel:
    @pytest.fixture
    def account(self):
        some_user = User(123, 'someone@gmail.com')
        return Account(456, some_user)

    def test_should_create_account_eith_right_balances(self):
        new_user = User(22, 'email@mail.com')
        new_account = Account(229, new_user)

        assert len(new_account.balances) == 3
        
        assert new_account.balances[BalanceType.CASH].amount == 0.00
        assert new_account.balances[BalanceType.FOOD].amount == 0.00
        assert new_account.balances[BalanceType.MEAL].amount == 0.00

    def test_should_credit_100_into_food_balance(self, account):
        assert len(account.balances) == 3

        account.credit(BalanceType.FOOD, 100.00)
        assert account.balances[BalanceType.FOOD].amount == 100.00

    def test_should_credit_100_then_debit_50_into_meal_balance(self, account):
        assert len(account.balances) == 3

        account.credit(BalanceType.MEAL, 100.00)
        account.debit(BalanceType.MEAL, 50.00)
        assert account.balances[BalanceType.MEAL].amount == 50.00


    def test_should_not_debit_when_no_enough_balance(self, account):
        assert len(account.balances) == 3

        with pytest.raises(NotEnoughBalanceException):
            account.debit(BalanceType.MEAL, 50.00)

