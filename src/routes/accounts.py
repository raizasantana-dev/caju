

from fastapi import APIRouter, Body, Request, status
from pydantic import BaseModel, EmailStr, Field

from src.domain.service.accounts import AccuntsService
from src.domain.model.account import Account


router = APIRouter(prefix="/account", tags=["Account"])
service = AccuntsService()

class CreateAccountRequest(BaseModel):
    email: EmailStr = Field(unique=True, index=True)
    
@router.post("/", response_description="Create a new account", status_code=status.HTTP_201_CREATED, response_model=Account)
def create_account(request: CreateAccountRequest = Body(...)):  
    return service.create(request)