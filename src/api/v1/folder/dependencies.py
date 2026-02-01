from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_folder_unit_of_work
from infrastructure.repositories.postgresql.folder.uow import PostgreSQLFolderUnitOfWork

from usecase.folder.create_folder.implementation import PostgreSQLCreateFolderUseCase
from usecase.folder.get_folders.implementation import PostgreSQLGetFoldersUseCase
from usecase.folder.update_folder.implementation import PostgreSQLUpdateFolderUseCase
from usecase.folder.delete_folder.implementation import PostgreSQLDeleteFolderUseCase


def get_folder_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLFolderUnitOfWork:
    return build_folder_unit_of_work(session)


def create_folder_use_case(
    uow: PostgreSQLFolderUnitOfWork = Depends(get_folder_unit_of_work),
) -> PostgreSQLCreateFolderUseCase:
    return PostgreSQLCreateFolderUseCase(uow=uow)


def get_folders_use_case(
    uow: PostgreSQLFolderUnitOfWork = Depends(get_folder_unit_of_work),
) -> PostgreSQLGetFoldersUseCase:
    return PostgreSQLGetFoldersUseCase(uow=uow)


def update_folder_use_case(
    uow: PostgreSQLFolderUnitOfWork = Depends(get_folder_unit_of_work),
) -> PostgreSQLUpdateFolderUseCase:
    return PostgreSQLUpdateFolderUseCase(uow=uow)


def delete_folder_use_case(
    uow: PostgreSQLFolderUnitOfWork = Depends(get_folder_unit_of_work),
) -> PostgreSQLDeleteFolderUseCase:
    return PostgreSQLDeleteFolderUseCase(uow=uow)