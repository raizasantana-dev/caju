from fastapi import APIRouter, Request, status
from fastapi import APIRouter
from src.routes import accounts

router = APIRouter()

health_check_router = APIRouter(prefix="/health",tags=["health-check"])
@health_check_router.get("/")
def health(request: Request):
    return { "ok": "ok"}

router.include_router(health_check_router)
router.include_router(accounts)