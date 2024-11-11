from enum import Enum
from pydantic import BaseModel, EmailStr, Field

from src.domain.model.balance import BalanceType


class CreateAccountRequest(BaseModel):
    email: EmailStr = Field(unique=True, index=True)

class UpdateBalanceOperation(Enum):
    CREDIT = 1
    DEBIT = 2
    
class UpdateAccountBalanceRequest(BaseModel):
    operation: UpdateBalanceOperation
    balance_type: BalanceType
    amount: float