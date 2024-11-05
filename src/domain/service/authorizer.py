from enum import Enum

from domain.model.account import Account
from domain.model.account_exceptions import NotEnoughBalanceException
from domain.model.balance import BalanceType
from domain.model.transaction import TransactionRequest
from domain.service.accounts import AccuntsService

class AuthorizationResult(Enum):
    AUTHORIZED = 1
    REJECTED_BALANCE = 2
    REJECTED_ERROR = 3


class TransactionsAuthorizer:
    def __init__(self) -> None:
        self.mcc_types = {
            '5411': BalanceType.FOOD,
            '5411': BalanceType.FOOD,
            '5811': BalanceType.MEAL,
            '5812': BalanceType.MEAL,
        }


    def authorize(self, request: TransactionRequest, account: Account) -> AuthorizationResult:
        
        transaction_type = self.mcc_types.get(request.mcc, BalanceType.CASH)

        try:
            self.accounts_service.debit(account, transaction_type, request.total_amount)
            return AuthorizationResult.AUTHORIZED
        except NotEnoughBalanceException:
            return AuthorizationResult.REJECTED_BALANCE
        except Exception:
            return AuthorizationResult.REJECTED_ERROR



       
