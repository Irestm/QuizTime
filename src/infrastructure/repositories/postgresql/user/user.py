import re

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.pydantic.models import CreateUserSchema, UserRead, UserLoginSchema
from api.v1.user.crypto import context
from infrastructure.databases.postgresql.models import User
from infrastructure.repositories.postgresql.user.exceptions import UserIsExist, UserNotFound


class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: CreateUserSchema) -> UserRead:
        user = User(
            username=payload.username,
            full_name=payload.full_name,
            password=payload.password,
            biography=payload.biography,
            email=payload.email,
        )
        self._session.add(user)
        try:
            await self._session.flush()
        except IntegrityError as e:
            pattern = r'Key \((.*?)\)=\((.*?)\)'
            match = re.search(pattern, str(e))
            if match:
                columns = [col.strip() for col in match.group(1).split(',')]
                values = [val.strip() for val in match.group(2).split(',')]
                raise UserIsExist(field=columns[0], value=values[0])
            raise e

        await self._session.refresh(user)
        return UserRead.model_validate(user)

    async def get(self, schema: UserLoginSchema) -> UserRead | None:
        query = select(User).where(and_(User.username == schema.username))
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()

        verify = context.verify(schema.password, user.password)

        if verify:
            return UserRead.model_validate(user)

        raise UserNotFound()

    async def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        return result.scalars().first()