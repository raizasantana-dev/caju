from fastapi import FastAPI
from src.routes.api import router

app = FastAPI()

app.include_router(router)