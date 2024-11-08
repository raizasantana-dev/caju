from enum import Enum
from datetime import datetime
import uuid

from pydantic import BaseModel, Field

class BalanceType(Enum):
    FOOD = 1
    MEAL = 2
    CASH = 3
    
class Balance(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    amount: float = 0.00
    type: BalanceType
    last_update: datetime = datetime.now()
    
