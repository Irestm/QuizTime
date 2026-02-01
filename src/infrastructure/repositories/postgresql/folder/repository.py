from typing import List

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.pydantic.models import FolderCreate, FolderUpdate, Pagination
from infrastructure.databases.postgresql.models import Folder
from infrastructure.repositories.postgresql.folder.exceptions import FolderNotFound


class PostgreSQLFolderRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: FolderCreate, user_id: int) -> Folder:
        # 1. Создаем объект
        folder = Folder(
            title=payload.title,
            description=payload.description,
            user_id=user_id
        )
        self._session.add(folder)
        await self._session.flush()

        query = (
            select(Folder)
            .options(selectinload(Folder.themes))
            .where(Folder.id == folder.id)
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_all(self, pagination: Pagination) -> List[Folder]:
        query = (
            select(Folder)
            .options(selectinload(Folder.themes))
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(self, folder_id: int, payload: FolderUpdate) -> Folder:
        values = payload.model_dump(exclude_unset=True)

        if not values:
            return await self._get_by_id(folder_id)

        stmt = (
            update(Folder)
            .where(Folder.id == folder_id)
            .values(**values)
            .returning(Folder.id)
        )
        result = await self._session.execute(stmt)
        updated_id = result.scalar_one_or_none()

        if not updated_id:
            raise FolderNotFound()

        return await self._get_by_id(updated_id)

    async def delete(self, folder_id: int) -> None:
        stmt = delete(Folder).where(Folder.id == folder_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise FolderNotFound()

    async def _get_by_id(self, folder_id: int) -> Folder:
        query = (
            select(Folder)
            .options(selectinload(Folder.themes))
            .where(Folder.id == folder_id)
        )
        result = await self._session.execute(query)
        folder = result.scalar_one_or_none()
        if not folder:
            raise FolderNotFound()
        return folder