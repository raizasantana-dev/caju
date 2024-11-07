from fastapi import FastAPI
from dotenv import dotenv_values
from fastapi.concurrency import asynccontextmanager
from pymongo import MongoClient
from src.routes.api import router
config = dotenv_values(".env")

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_user = config['MONGO_INITDB_ROOT_USERNAME']
    db_pass = config['MONGO_INITDB_ROOT_PASSWORD']
    uri = f'mongodb://{db_user}:{db_pass}@mongodb:27017'
    app.mongodb_client = MongoClient(uri)
    app.database = app.mongodb_client[config["MONGO_INITDB_ROOT_DB_NAME"]]
    yield
    app.mongodb_client.close()
    

app.include_router(router)