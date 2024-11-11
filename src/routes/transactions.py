
from fastapi import APIRouter, Body, status

from src.domain.service.authorizer import TransactionsAuthorizer
from src.domain.model.transaction import TransactionRequest


router = APIRouter(prefix="/transaction", tags=["Transaction"])
service = TransactionsAuthorizer()

@router.post("/", response_description="Create a new transaction", status_code=status.HTTP_200_OK)
def create_transaction(request: TransactionRequest = Body(...)):  
    code = service.authorize(request)
    return {'code': code}