from fastapi import APIRouter

from .views import router as folder_router

router = APIRouter(tags=["Folder"])

router.include_router(folder_router)
