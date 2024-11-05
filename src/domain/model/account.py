
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
            BalanceType.FOOD: Balance(0.00),
            BalanceType.MEAL: Balance(0.00),
            BalanceType.CASH: Balance(0.00)
        }
        self.card_list = []


    def get_balance(self, type) -> Balance:
        return self.balances[type]
    
    def debit(self, type, total_amount):
        self.balances[type].amount -= total_amount

    def credit(self, type, total_amount):
        self.balances[type].amount += total_amount




    