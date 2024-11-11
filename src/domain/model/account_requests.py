from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class CreateAccountRequest(BaseModel):
    email: EmailStr = Field(unique=True, index=True)

class Operation(Enum):
    DEBIT = 1
    CREDIT = 2
    
class UpdateAccountBalanceRequest(BaseModel):
   balance_type: str
   operation: Operation
   amount: float