from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.repositories.postgresql.user import PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgresql.folder import PostgreSQLFolderUnitOfWork
from infrastructure.repositories.postgresql.theme import PostgreSQLThemeUnitOfWork


def build_user_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLUserUnitOfWork:
    return Container.user_uow_factory(session=session)


def build_folder_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLFolderUnitOfWork:
    return Container.folder_uow_factory(session=session)


def build_theme_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLThemeUnitOfWork:
    return Container.theme_uow_factory(session=session)