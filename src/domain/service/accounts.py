from src.domain.model.account import Account, User
from src.domain.model.balance import Balance, BalanceType
from src.repository.mongodb import account as accounts_repository


class AccountsService:
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
    
    def debit(self, account_id, balance_type, amount):
        account = accounts_repository.find_account(account_id)
        new_balance = account.debit(balance_type, amount)

        accounts_repository.update_balance(account, new_balance)
        return account

    def credit(self, account_id, balance_type, amount):
        account = accounts_repository.find_account(account_id)
        new_balance = account.credit(balance_type, amount)

        accounts_repository.update_balance(account, new_balance)
        return account
