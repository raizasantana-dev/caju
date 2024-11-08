

from fastapi import APIRouter, Body, Request, status

from src.domain.model.account import Account
import src.domain.service.accounts as accounts_service

router = APIRouter(prefix="/account", tags=["Account"])


@router.post("/", response_description="Create a new account", status_code=status.HTTP_201_CREATED)
def create_account(account: Account = Body(...)):  
    return accounts_service.create_account(account)