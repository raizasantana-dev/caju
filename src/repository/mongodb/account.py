from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from src.repository.mongodb.helper import get_collection
from src.domain.model.account import Account

def get_collection_accounts():
  return get_collection("accounts")

def create_account(account: Account):
    account = jsonable_encoder(account)
    new_account = get_collection_accounts().insert_one(account)
    created_account = get_collection_accounts().find_one({"_id": new_account.inserted_id})
    return created_account
