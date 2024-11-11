from enum import Enum
from datetime import datetime
import uuid

from pydantic import BaseModel, Field

class BalanceType(Enum):
    FOOD = "FOOD"
    MEAL = "MEAL"
    CASH = "CASH"
    
class Balance(BaseModel):
    amount: float = 0.00
    type: BalanceType = Field()
    last_update: datetime = datetime.now()
    
