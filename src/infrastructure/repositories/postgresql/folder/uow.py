from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repositories.postgresql.folder.repository import PostgreSQLFolderRepository

class PostgreSQLFolderUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self.folder: PostgreSQLFolderRepository | None = None

    async def __aenter__(self):
        self.folder = PostgreSQLFolderRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

        self.folder = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()