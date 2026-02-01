from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import JSONResponse

from api.pydantic.models import ThemeCreate, ThemeResponse, ThemeUpdate
from infrastructure.repositories.postgresql.folder.exceptions import FolderNotFound
from infrastructure.repositories.postgresql.theme.exceptions import ThemeNotFound
from infrastructure.databases.postgresql.models import User

from usecase.theme.create_theme.abstract import AbstractCreateThemeUseCase
from usecase.theme.update_theme.abstract import AbstractUpdateThemeUseCase
from usecase.theme.delete_theme.abstract import AbstractDeleteThemeUseCase
from usecase.theme.get_theme.abstract import AbstractGetThemeUseCase

from api.v1.auth.dependencies import get_current_user
from api.v1.theme.dependencies import (
    create_theme_use_case,
    update_theme_use_case,
    delete_theme_use_case,
    get_theme_use_case
)

router = APIRouter(tags=["Theme"])

@router.post("/folders/{folder_id}/themes", response_model=ThemeResponse)
async def create_theme(
        folder_id: int,
        payload: ThemeCreate,
        current_user: User = Depends(get_current_user),
        usecase: AbstractCreateThemeUseCase = Depends(create_theme_use_case)
) -> JSONResponse:
    try:
        theme = await usecase.execute(folder_id, payload, user_id=current_user.id)
    except FolderNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=theme.model_dump()
    )

@router.patch("/themes/{theme_id}", response_model=ThemeResponse)
async def update_theme(
        theme_id: int,
        payload: ThemeUpdate,
        current_user: User = Depends(get_current_user),
        usecase: AbstractUpdateThemeUseCase = Depends(update_theme_use_case)
) -> JSONResponse:
    try:
        updated_theme = await usecase.execute(theme_id, payload, user_id=current_user.id)
    except ThemeNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_theme.model_dump()
    )

@router.delete("/themes/{theme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_theme(
        theme_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractDeleteThemeUseCase = Depends(delete_theme_use_case)
):
    try:
        await usecase.execute(theme_id, user_id=current_user.id)
    except ThemeNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/themes/{theme_id}", response_model=ThemeResponse)
async def get_theme(
        theme_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetThemeUseCase = Depends(get_theme_use_case)
) -> JSONResponse:
    try:
        theme = await usecase.execute(theme_id, user_id=current_user.id)
    except ThemeNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=theme.model_dump()
    )