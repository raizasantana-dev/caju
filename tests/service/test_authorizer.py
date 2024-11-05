
from pytest import fixture

from src.domain.model.account import Account, User
from src.domain.model.balance import BalanceType
from src.domain.model.transaction import TransactionRequest
from src.domain.service.authorizer import AuthorizationResult, TransactionsAuthorizer


class TestAuthorizerService:
    @fixture
    def service(self):
        return TransactionsAuthorizer()
    
    @fixture
    def account(self):
        some_user = User(123, 'someone@gmail.com')
        return Account(456, some_user)
    

    def test_should_not_authorized_transaction(self, account, service):
        assert account.get_balance(BalanceType.CASH).amount == 0.00

        transaction_request = TransactionRequest(
            account.id,
            23.90,
            '1234',
            'Padaria Silva'
        )
        
        result = service.authorize(transaction_request, account)

        assert result == AuthorizationResult.REJECTED_BALANCE