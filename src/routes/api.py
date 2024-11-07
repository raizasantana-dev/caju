from fastapi import APIRouter, Request, status

router = APIRouter(prefix="/health",tags=["health-check"])

@router.get("/")
def health(request: Request):
    return { "ok": "ok"}