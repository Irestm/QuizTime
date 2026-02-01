from fastapi import HTTPException, status
from api.pydantic.models import ThemeUpdate, ThemeResponse
from infrastructure.repositories.postgresql.theme.uow import PostgreSQLThemeUnitOfWork
from .abstract import AbstractUpdateThemeUseCase


class PostgreSQLUpdateThemeUseCase(AbstractUpdateThemeUseCase):
    def __init__(self, uow: PostgreSQLThemeUnitOfWork):
        self._uow = uow

    async def execute(self, theme_id: int, theme_payload: ThemeUpdate, user_id: int) -> ThemeResponse:
        async with self._uow as uow:
            theme = await uow.theme._get_by_id(theme_id)
            folder = await uow.folder._get_by_id(theme.folder_id)

            if folder.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )

            updated_theme = await uow.theme.update(theme_id, theme_payload)
            response = ThemeResponse.model_validate(updated_theme)
            await uow.commit()
            return response