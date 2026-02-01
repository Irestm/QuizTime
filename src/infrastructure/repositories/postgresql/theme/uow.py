from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repositories.postgresql.theme.repository import PostgreSQLThemeRepository
from infrastructure.repositories.postgresql.folder.repository import PostgreSQLFolderRepository

class PostgreSQLThemeUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.theme = PostgreSQLThemeRepository(session)
        self.folder = PostgreSQLFolderRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()