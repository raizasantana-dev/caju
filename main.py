from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from src.repository.mongodb.helper import get_collection, get_mongo_client
from src.routes.api import router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = get_mongo_client()
    yield
    app.mongodb_client.close()
    

app.include_router(router)