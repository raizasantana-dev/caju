
from typing import List, Optional
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType


class User(BaseModel):
    email: EmailStr = Field()

class Account(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    user: User
    balances: List[Balance]

    model_config = ConfigDict(
            populate_by_name = True,
            )
        

    def get_balance(self, type) -> Balance:
       for balance in self.balances:
           if balance.type == type:
               return balance
    
    def debit(self, type, total_amount): 

        current_amount = self.get_balance(type).amount
        if (current_amount < total_amount):
            
            cash_balance = self.get_balance(BalanceType.CASH).amount
            if (cash_balance < total_amount):
                raise NotEnoughBalanceException()
            else:
                self.get_balance(BalanceType.CASH).amount -= total_amount
        else:
            self.get_balance(type).amount -= total_amount

    def credit(self, type, total_amount):
        right_balance = self.get_balance(type)
        right_balance.amount += total_amount




    