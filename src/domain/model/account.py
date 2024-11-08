
import uuid
from pydantic import BaseModel, EmailStr, Field
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    email: EmailStr = Field(unique=True, index=True)
    

class Account(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    user: User
    balances: dict[BalanceType, Balance] = {
            BalanceType.FOOD: Balance(type=BalanceType.FOOD),
            BalanceType.MEAL: Balance(type=BalanceType.MEAL),
            BalanceType.CASH: Balance(type=BalanceType.CASH)
    } 

    def get_balance(self, type) -> Balance:
        return self.balances[type]
    
    def debit(self, type, total_amount): 
        current_amount = self.balances[type].amount
        if (current_amount < total_amount):
            
            cash_balance = self.balances[BalanceType.CASH].amount
            if (cash_balance < total_amount):
                raise NotEnoughBalanceException()
            else:
                self.balances[BalanceType.CASH].amount -= total_amount
        else:
            self.balances[type].amount -= total_amount

    def credit(self, type, total_amount):
        self.balances[type].amount += total_amount




    