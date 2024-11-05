
class TransactionRequest:
    def __init__(self, account_id, total_amount, mcc, merchant):
        self.account_id = account_id
        self.total_amount = total_amount
        self.mcc = mcc
        self.merchant = merchant