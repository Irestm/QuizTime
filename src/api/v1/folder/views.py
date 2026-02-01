from typing import List

from fastapi import APIRouter, Depends, status, Query, HTTPException, Response
from fastapi.responses import JSONResponse

from api.pydantic.models import FolderCreate, FolderResponse, Pagination, FolderUpdate
from api.v1.auth.dependencies import get_current_user
from api.v1.folder.dependencies import (
    create_folder_use_case,
    get_folders_use_case,
    update_folder_use_case,
    delete_folder_use_case
)
from infrastructure.databases.postgresql.models import User
from infrastructure.repositories.postgresql.folder.exceptions import FolderNotFound
from usecase.folder.create_folder.abstract import AbstractCreateFolderUseCase
from usecase.folder.get_folders.abstract import AbstractGetFoldersUseCase
from usecase.folder.update_folder.abstract import AbstractUpdateFolderUseCase
from usecase.folder.delete_folder.abstract import AbstractDeleteFolderUseCase

router = APIRouter(tags=["Folder"])


@router.post("/folders", response_model=FolderResponse)
async def create_folder(
        payload: FolderCreate,
        current_user: User = Depends(get_current_user),
        usecase: AbstractCreateFolderUseCase = Depends(create_folder_use_case)
) -> JSONResponse:
    folder = await usecase.execute(payload, user_id=current_user.id)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=folder.model_dump()
    )


@router.get("/folders", response_model=List[FolderResponse])
async def get_my_folders(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        current_user: User = Depends(get_current_user),
        usecase: AbstractGetFoldersUseCase = Depends(get_folders_use_case)
) -> JSONResponse:
    pagination = Pagination(limit=limit, offset=offset)
    folders = await usecase.execute(pagination)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[f.model_dump() for f in folders]
    )


@router.patch("/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(
        folder_id: int,
        payload: FolderUpdate,
        current_user: User = Depends(get_current_user),
        usecase: AbstractUpdateFolderUseCase = Depends(update_folder_use_case)
) -> JSONResponse:
    try:
        updated_folder = await usecase.execute(folder_id, payload)
    except FolderNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_folder.model_dump()
    )


@router.delete("/folders/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(
        folder_id: int,
        current_user: User = Depends(get_current_user),
        usecase: AbstractDeleteFolderUseCase = Depends(delete_folder_use_case)
):
    try:
        await usecase.execute(folder_id)
    except FolderNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)