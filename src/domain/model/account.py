
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: EmailStr = Field(unique=True, index=True)

    

class Account(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user: User
    balances: dict[BalanceType, Balance]

    model_config = ConfigDict(
            populate_by_name = True,
            )
        

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




    