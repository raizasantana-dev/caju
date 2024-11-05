from enum import Enum
from datetime import datetime

class BalanceType(Enum):
    FOOD = 1
    MEAL = 2
    CASH = 3

    # def _is_food(mcc) -> bool:
    #     return mcc in ["5411", "5412"]
    
    # def _is_meal(mcc) -> bool:
    #     return mcc in ["5811", "5812"]
    
class Balance:
    def __init__(self, initial_amount = 0.00):
        self.amount = initial_amount
        # self.locked = False
        self.last_update = datetime.now()


    # def lock(self):
    #     self.locked = True
    #     self.last_update = datetime.now()


    # def un_lock(self):
    #     self.locked = False
    #     self.last_update = datetime.now()
