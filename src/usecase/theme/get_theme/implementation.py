from fastapi import HTTPException, status
from api.pydantic.models import ThemeResponse
from infrastructure.repositories.postgresql.theme.uow import PostgreSQLThemeUnitOfWork
from .abstract import AbstractGetThemeUseCase

class PostgreSQLGetThemeUseCase(AbstractGetThemeUseCase):
    def __init__(self, uow: PostgreSQLThemeUnitOfWork):
        self._uow = uow

    async def execute(self, theme_id: int, user_id: int) -> ThemeResponse:
        async with self._uow as uow:
            theme = await uow.theme._get_by_id(theme_id)
            folder = await uow.folder._get_by_id(theme.folder_id)

            if folder.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )

            return ThemeResponse.model_validate(theme)