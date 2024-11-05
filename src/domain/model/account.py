
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType


class User:
    def __init__(self, id, email) -> None:
        self.id = id
        self.email = email

class Account:
    def __init__(self, id, user: User) -> None:
        self.id = id
        self.user = User
        self.balances: dict[BalanceType, Balance] = {
            BalanceType.FOOD: Balance(BalanceType.FOOD),
            BalanceType.MEAL: Balance(BalanceType.MEAL),
            BalanceType.CASH: Balance(BalanceType.CASH)
        }
        self.card_list = []


    def get_balance(self, type) -> Balance:
        return self.balances[type]
    
    def debit(self, type, total_amount): # TODO: this mehotd should be global
        current_amount = self.balances[type].amount
        if (current_amount < total_amount):
            raise NotEnoughBalanceException()
        else:
            self.balances[type].amount -= total_amount

    def credit(self, type, total_amount):
        self.balances[type].amount += total_amount




    