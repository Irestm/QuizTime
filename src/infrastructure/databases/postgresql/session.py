from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from container import Container
from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager

@inject
async def get_async_session(
    sessionmanager: DatabaseSessionManager = Depends(Provide[Container.session_manager]),
) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session