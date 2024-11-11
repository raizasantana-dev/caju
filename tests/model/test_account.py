
import pytest
from src.domain.model.account import Account, User
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType


class TestAccountModel:
    @pytest.fixture
    def account(self):
        some_user = User(email='someone@gmail.com')
        balances=[
               Balance(type=BalanceType.FOOD),
               Balance(type=BalanceType.MEAL),
               Balance(type=BalanceType.CASH)
            ]
        return Account(user=some_user, balances=balances)

    def test_should_credit_100_into_food_balance(self, account):
        assert len(account.balances) == 3

        account.credit(BalanceType.FOOD, 100.00)
        assert account.get_balance(BalanceType.FOOD).amount == 100.00

    def test_should_credit_100_then_debit_50_into_meal_balance(self, account):
        assert len(account.balances) == 3

        account.credit(BalanceType.MEAL, 100.00)
        account.debit(BalanceType.MEAL, 50.00)
        assert account.get_balance(BalanceType.MEAL).amount == 50.00


    def test_should_not_debit_when_no_enough_balance(self, account):
        assert len(account.balances) == 3

        with pytest.raises(NotEnoughBalanceException):
            account.debit(BalanceType.MEAL, 50.00)


    def test_should_get_correct_balance(self, account):
        result = account.get_balance(BalanceType.CASH)
        assert result.type == BalanceType.CASH
        assert result.amount == 0.00
