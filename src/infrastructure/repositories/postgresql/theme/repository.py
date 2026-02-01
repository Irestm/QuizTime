from typing import List
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.pydantic.models import ThemeCreate, ThemeUpdate
from infrastructure.databases.postgresql.models import Theme, QuizItem, MemorizeItem
from infrastructure.repositories.postgresql.theme.exceptions import ThemeNotFound


class PostgreSQLThemeRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, folder_id: int, payload: ThemeCreate) -> Theme:
        theme = Theme(
            title=payload.title,
            type=payload.type,
            folder_id=folder_id
        )
        self._session.add(theme)
        await self._session.flush()

        if payload.quiz_items:
            for item in payload.quiz_items:
                qi = QuizItem(
                    question=item.question,
                    answers=item.answers,
                    true_answer=item.true_answer,
                    theme_id=theme.id
                )
                self._session.add(qi)

        if payload.memorize_items:
            for item in payload.memorize_items:
                mi = MemorizeItem(
                    word=item.word,
                    translate=item.translate,
                    transcription=item.transcription,
                    theme_id=theme.id
                )
                self._session.add(mi)

        await self._session.flush()

        return await self._get_by_id(theme.id)

    async def update(self, theme_id: int, payload: ThemeUpdate) -> Theme:
        values = payload.model_dump(exclude_unset=True)

        if not values:
            return await self._get_by_id(theme_id)

        stmt = (
            update(Theme)
            .where(Theme.id == theme_id)
            .values(**values)
            .returning(Theme.id)
        )
        result = await self._session.execute(stmt)
        updated_id = result.scalar_one_or_none()

        if not updated_id:
            raise ThemeNotFound()

        return await self._get_by_id(updated_id)

    async def delete(self, theme_id: int) -> None:
        stmt = delete(Theme).where(Theme.id == theme_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise ThemeNotFound()

    async def _get_by_id(self, theme_id: int) -> Theme:
        query = (
            select(Theme)
            .options(
                selectinload(Theme.quiz_items),
                selectinload(Theme.memorize_items)
            )
            .where(Theme.id == theme_id)
        )
        result = await self._session.execute(query)
        theme = result.scalar_one_or_none()

        if not theme:
            raise ThemeNotFound()

        return theme

    async def get(self, theme_id: int) -> Theme:
        return await self._get_by_id(theme_id)