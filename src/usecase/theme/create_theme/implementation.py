from fastapi import HTTPException, status
from api.pydantic.models import ThemeCreate, ThemeResponse
from infrastructure.repositories.postgresql.folder.uow import PostgreSQLFolderUnitOfWork
from .abstract import AbstractCreateThemeUseCase


class PostgreSQLCreateThemeUseCase(AbstractCreateThemeUseCase):
    def __init__(self, uow: PostgreSQLFolderUnitOfWork):
        self._uow: PostgreSQLFolderUnitOfWork = uow

    async def execute(self, folder_id: int, theme: ThemeCreate, user_id: int) -> ThemeResponse:
        async with self._uow as uow:
            folder = await uow.folder._get_by_id(folder_id)

            if folder.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to access this folder"
                )

            created_theme = await uow.theme.create(folder_id, theme)
            response = ThemeResponse.model_validate(created_theme)
            await uow.commit()

            return response