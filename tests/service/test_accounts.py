from unittest.mock import MagicMock
from pytest import fixture

from src.domain.model.account import Account, User
from src.domain.model.balance import Balance, BalanceType
from src.domain.service.accounts import AccountsService
from src.repository.mongodb import account as accounts_repository



class TestAccountsService:
    @fixture
    def service(self):
        return AccountsService()
    
    @fixture
    def repository(self):
           return accounts_repository
    
    @fixture
    def account(self):
        some_user = User(email='someone@gmail.com')
        balances=[
               Balance(type=BalanceType.FOOD),
               Balance(type=BalanceType.MEAL),
               Balance(type=BalanceType.CASH)
            ]
        return Account(user=some_user, balances=balances)   
    

    def test_should_credit_food_balance(self, account, service, repository):
            repository.find_account = MagicMock(return_value=account)

            repository.update_balance = MagicMock(account)

            result = service.credit(account.id, BalanceType.FOOD, 300)

            assert result == account
            assert result.get_balance(BalanceType.FOOD).amount == 300


    def test_should_debit_cash_balance(self, account, service, repository):
            repository.find_account = MagicMock(return_value=account)
            repository.update_balance = MagicMock(account)

            result_credit = service.credit(account.id, BalanceType.CASH, 300)
            assert result_credit.get_balance(BalanceType.CASH).amount == 300

            result_debit = service.debit(account.id, BalanceType.CASH, 200)
            assert result_debit.get_balance(BalanceType.CASH).amount == 100
        