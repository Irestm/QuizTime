from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgresql.user.uow import PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgresql.folder.uow import PostgreSQLFolderUnitOfWork
from infrastructure.repositories.postgresql.theme.uow import PostgreSQLThemeUnitOfWork


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    user_uow_factory = Factory(PostgreSQLUserUnitOfWork)
    folder_uow_factory = Factory(PostgreSQLFolderUnitOfWork)
    theme_uow_factory = Factory(PostgreSQLThemeUnitOfWork)