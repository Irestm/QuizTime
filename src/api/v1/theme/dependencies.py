from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_theme_unit_of_work
from infrastructure.repositories.postgresql.theme.uow import PostgreSQLThemeUnitOfWork

from usecase.theme.create_theme.implementation import PostgreSQLCreateThemeUseCase
from usecase.theme.update_theme.implementation import PostgreSQLUpdateThemeUseCase
from usecase.theme.delete_theme.implementation import PostgreSQLDeleteThemeUseCase
from usecase.theme.get_theme.implementation import PostgreSQLGetThemeUseCase

def get_theme_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLThemeUnitOfWork:
    return build_theme_unit_of_work(session)


def create_theme_use_case(
    uow: PostgreSQLThemeUnitOfWork = Depends(get_theme_unit_of_work),
) -> PostgreSQLCreateThemeUseCase:
    return PostgreSQLCreateThemeUseCase(uow=uow)


def update_theme_use_case(
    uow: PostgreSQLThemeUnitOfWork = Depends(get_theme_unit_of_work),
) -> PostgreSQLUpdateThemeUseCase:
    return PostgreSQLUpdateThemeUseCase(uow=uow)


def delete_theme_use_case(
    uow: PostgreSQLThemeUnitOfWork = Depends(get_theme_unit_of_work),
) -> PostgreSQLDeleteThemeUseCase:
    return PostgreSQLDeleteThemeUseCase(uow=uow)


def get_theme_use_case(
    uow: PostgreSQLThemeUnitOfWork = Depends(get_theme_unit_of_work),
) -> PostgreSQLGetThemeUseCase:
    return PostgreSQLGetThemeUseCase(uow=uow)