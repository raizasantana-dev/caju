from src.domain.model.account import Account
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType


class AccuntsService:
    def get_account(self, id) -> Account:
        return Account(1, 'rose@mail.com')
    
    # def get_balance_locked(self, account_id, type: BalanceType) -> Balance:
    #     balance_list = self.get_account(account_id).balance_list
    
    def debit(self, account, balance_type, total_amount):
        account.debit(balance_type, total_amount)
