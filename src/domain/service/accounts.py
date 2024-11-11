import uuid
from src.domain.model.account import Account, User
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import Balance, BalanceType
from src.repository.mongodb import account as accounts_repository


class AccuntsService:
    def get_account(self, id) -> Account:
        return accounts_repository.find_account(id)
    
    def create(self, request) -> Account:
        account = Account(
            user=User(email=request.email),
            balances=[
               Balance(type=BalanceType.FOOD),
               Balance(type=BalanceType.MEAL),
               Balance(type=BalanceType.CASH)
            ]
        )

        return accounts_repository.insert_account(account)
    
    def debit(self, account, balance_type, total_amount):
        account.debit(balance_type, total_amount)

    def credit(self, account, balance_type, total_amount):
        account.credit(balance_type, total_amount)