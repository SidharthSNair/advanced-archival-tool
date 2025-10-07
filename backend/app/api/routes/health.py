from fastapi import APIRouter
from app.core.config import app_info

router = APIRouter(tags=["system"])

@router.get("/health")
def health():
    # Minimal health signal; later we might ping DB, etc.
    return {"status": "ok", "service": app_info.name, "version": app_info.version}

@router.get("/info")
def info():
    return app_info.model_dump()
