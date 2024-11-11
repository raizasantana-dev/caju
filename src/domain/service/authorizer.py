from enum import Enum
import re

from src.domain.model.account import Account
from src.domain.model.account_exceptions import NotEnoughBalanceException
from src.domain.model.balance import BalanceType
from src.domain.model.transaction import TransactionRequest
from src.domain.service.accounts import AccountsService


FOOD_RGX ="\\b(EXTRA|PAO\\s*DE\\s*ACUCAR|CARREFOUR|ASSAI|DIA|ATACADAO|MAKRO|SAMS\\s*CLUB|GUANABARA|BRETAS|ANGELONI|CONDOR|SUPER\\s*BOM|ZAFFARI|SONDA|TAUSTE|BIG\\s*BOMPRECO)\\b"
MEAL_RGX = '\\b(MC\\s*DONALDS?|BURGER\\s*KING|UBER\\s*EATS|SUBWAY|OUTBACK|STARBUCKS|PIZZA\\s*HUT|DOMINOS|KFC|GIRAFFAS|HABIBS|BOB\\s*S|RAGAZZO|COCO\\s*BAMBU|MADERO|MADEIRO|CHINA\\s*IN\\s*BOX|VIVENDA\\s*DO\\s*CAMARAO|SPOLETO|GRILLE?)\\b'

class AuthorizationResult(Enum):
    AUTHORIZED = "00"
    REJECTED_BALANCE = "51"
    REJECTED_ERROR = "07"


class TransactionsAuthorizer:
    def __init__(self) -> None:
        self.mcc_types = {
            '5411': BalanceType.FOOD,
            '5411': BalanceType.FOOD,
            '5811': BalanceType.MEAL,
            '5812': BalanceType.MEAL,
        }
        self.accounts_service = AccountsService()

    def authorize(self, request: TransactionRequest) -> AuthorizationResult:
        account = self.accounts_service.get_account(request.account_id)
        transaction_type = self.extract_type(request)

        try:
            self.accounts_service.debit(account.id, transaction_type, request.total_amount)
            return AuthorizationResult.AUTHORIZED
        except NotEnoughBalanceException:
            return AuthorizationResult.REJECTED_BALANCE
        except Exception as ex:
            print(str(ex))
            return AuthorizationResult.REJECTED_ERROR
        
    def extract_type(self, request: TransactionRequest) -> BalanceType:
        if (re.search(FOOD_RGX, request.merchant.upper())):
            return BalanceType.FOOD
        elif (re.search(MEAL_RGX, request.merchant.upper())):
            return BalanceType.MEAL
        else:
            return self.mcc_types.get(request.mcc, BalanceType.CASH)



       
