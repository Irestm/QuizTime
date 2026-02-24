import multiprocessing
from contextlib import asynccontextmanager
from typing import AsyncIterator

import psutil
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncConnection,
    AsyncEngine
)

from .base import Base


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(
            host,
            pool_size=50,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=False,
            connect_args={
                "prepared_statement_cache_size": 0,
                "statement_cache_size": 0
            }
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            bind=self._engine,
            expire_on_commit=False
        )

    async def tune_postgres_for_hardware(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        mem = psutil.virtual_memory()
        total_ram_gb = mem.total / (1024**3)
        cpu_threads = multiprocessing.cpu_count()

        shared_buffers = f"{int(total_ram_gb * 0.25)}GB"
        effective_cache_size = f"{int(total_ram_gb * 0.75)}GB"
        work_mem = f"{int((mem.total / 1024 / 1024) / (cpu_threads * 4))}MB"
        max_connections = cpu_threads * 20

        tuning_commands = [
            f"ALTER SYSTEM SET shared_buffers = '{shared_buffers}';",
            f"ALTER SYSTEM SET effective_cache_size = '{effective_cache_size}';",
            f"ALTER SYSTEM SET work_mem = '{work_mem}';",
            "ALTER SYSTEM SET synchronous_commit = off;",
            f"ALTER SYSTEM SET max_connections = {max_connections};",
            "SELECT pg_reload_conf();"
        ]

        async with self.connect() as conn:
            for cmd in tuning_commands:
                try:
                    await conn.execute(text(cmd))
                except Exception:
                    pass

    async def close(self):
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)