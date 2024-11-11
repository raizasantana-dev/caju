
from pydantic import BaseModel


class TransactionRequest(BaseModel):
        account_id: str
        total_amount: float
        mcc: str
        merchant: str