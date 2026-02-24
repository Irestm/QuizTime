from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from usecase.create_token.implementation import PostgreSQLCreateTokenUseCase
from infrastructure.di.injection import build_user_unit_of_work
from api.pydantic.models import UserLoginSchema
from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.repositories.postgresql.user.user import PostgreSQLUserRepository

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
):
    uow = build_user_unit_of_work(session)
    usecase = PostgreSQLCreateTokenUseCase(uow)

    user_login = UserLoginSchema(
        username=form_data.username,
        password=form_data.password
    )

    token_data = await usecase.execute(user_login)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": token_data.access_token,
        "token_type": "bearer"
    }


@router.post("/bulk-generate")
async def bulk_generate_users(
        count: int,
        session: AsyncSession = Depends(get_async_session)
):
    repo = PostgreSQLUserRepository(session)
    result = await repo.bulk_create_users(count)

    return {
        "status": "success",
        "message": f"Generated {result} users with unique hashes",
        "count": result
    }