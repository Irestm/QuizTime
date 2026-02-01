from contextlib import asynccontextmanager

from fastapi import FastAPI

from settings import settings
from api.v1 import routers as api_v1
from container import Container

container = Container()

@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager = container.session_manager()
    sessionmanager.init(settings.database.get_database_url())

    async with sessionmanager.connect() as conn:
        await sessionmanager.create_all(conn)

    try:
        yield
    finally:
        await sessionmanager.close()

container.wire(
    modules=[
        "infrastructure.databases.postgresql.session",
        "api.v1.user.dependencies",
        "api.v1.theme.dependencies",
    ]
)

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1.router)