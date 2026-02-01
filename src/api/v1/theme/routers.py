from fastapi import APIRouter

from .views import router as theme_router

router = APIRouter(tags=["Theme"])

router.include_router(theme_router)
