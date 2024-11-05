
from src.domain.model.account import Account, User
from src.domain.model.balance import BalanceType


class TestAccountModel:

    def test_should_create_account_eith_right_balances(self):
        new_user = User(22, 'email@mail.com')
        new_account = Account(229, new_user)

        assert len(new_account.balances) == 3

    def test_should_credit_100_into_food_balance(self):
        new_user = User(22, 'email@mail.com')
        new_account = Account(229, new_user)

        assert len(new_account.balances) == 3

        new_account.credit(BalanceType.FOOD, 100.00)
        assert new_account.balances[BalanceType.FOOD].amount == 100.00

    def test_should_credit_100_then_debit50_into_meal_balance(self):
        new_user = User(22, 'email@mail.com')
        new_account = Account(229, new_user)

        assert len(new_account.balances) == 3

        new_account.credit(BalanceType.MEAL, 100.00)
        new_account.debit(BalanceType.MEAL, 50.00)
        assert new_account.balances[BalanceType.MEAL].amount == 50.00

