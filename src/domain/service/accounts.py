from src.domain.model.account import Account
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType
from src.repository.mongodb import account as accounts_repository


class AccuntsService:
    def get_account(self, id) -> Account:
        return Account(1, 'rose@mail.com')
    
    def create(self, account) -> Account:
        return accounts_repository.create_account(account)
    
    def debit(self, account, balance_type, total_amount):
        account.debit(balance_type, total_amount)

    def credit(self, account, balance_type, total_amount):
        account.credit(balance_type, total_amount)