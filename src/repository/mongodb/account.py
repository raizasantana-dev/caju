from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from src.repository.mongodb.helper import get_collection
from src.domain.model.account import Account

def get_collection_accounts():
  return get_collection("accounts")

def insert_account(account_instance):
    account_data = jsonable_encoder(account_instance) 
    result = get_collection_accounts().insert_one(account_data)
    print(f"Account inserted with _id: {result.inserted_id}")
    return str(result.inserted_id)


def find_account( id: str):
    if (account := get_collection_accounts().find_one({"_id": id})):
        return account
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account with id {id} not found!")