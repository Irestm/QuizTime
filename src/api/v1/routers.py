from fastapi import APIRouter

from api.v1.user.routers import router as user_router
from api.v1.folder.routers import router as folder_router
from api.v1.theme.routers import router as theme_router
from api.v1.auth.routers import router as auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(user_router)
router.include_router(folder_router)
router.include_router(theme_router)
router.include_router(auth_router)