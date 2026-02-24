import asyncio
from infrastructure.databases.postgresql.base import Base
from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager
from settings import settings

async def init():
    mgr = DatabaseSessionManager()
    mgr.init(settings.get_database_url().replace("asyncpg", "asyncpg"))
    async with mgr.connect() as conn:
        await mgr.create_all(conn)
    print("Tables created!")

if __name__ == "__main__":
    asyncio.run(init())