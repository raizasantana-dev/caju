

from enum import Enum
from fastapi import APIRouter, Body, Request, status
from pydantic import BaseModel, EmailStr, Field

from src.domain.model.balance import BalanceType
from src.domain.service.accounts import AccountsService
from src.domain.model.account import Account


router = APIRouter(prefix="/account", tags=["Account"])
service = AccountsService()

class CreateAccountRequest(BaseModel):
    email: EmailStr = Field(unique=True, index=True)

class UpdateBalanceOperation(Enum):
    CREDIT = 1
    DEBIT = 2
    
class UpdateAccountBalanceRequest(BaseModel):
    operation: UpdateBalanceOperation
    balance_type: BalanceType
    amount: float
    
@router.post("/", response_description="Create a new account", status_code=status.HTTP_201_CREATED)
def create_account(request: CreateAccountRequest = Body(...)):  
    return service.create(request)

@router.get("/{id}", response_description="Get a single account by id", response_model=Account)
def find_user(id: str):    
    return service.get_account(id)


@router.post("/{id}/balance", response_description="Update an account balance", status_code=status.HTTP_200_OK)
def update_account_balance(id: str, request: UpdateAccountBalanceRequest = Body(...)):  
    if (request.operation == UpdateBalanceOperation.CREDIT):
        return service.credit(id, request.balance_type, request.amount)
    else:
        return service.debit(id, request.balance_type, request.amount)