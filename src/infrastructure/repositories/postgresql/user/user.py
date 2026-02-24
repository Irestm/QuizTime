import re
import time
from concurrent.futures import ProcessPoolExecutor

from sqlalchemy import select, and_, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.pydantic.models import CreateUserSchema, UserRead, UserLoginSchema
from api.v1.user.crypto import context
from infrastructure.databases.postgresql.models import User
from infrastructure.repositories.postgresql.user.exceptions import UserIsExist, UserNotFound


def _hash_worker(password: str) -> str:
    return context.hash(password)


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

    async def bulk_create_users(self, count: int = 1000):
        run_id = int(time.time())
        raw_passwords = [f"password_{run_id}_{i}" for i in range(count)]

        with ProcessPoolExecutor() as executor:
            hashed_passwords = list(executor.map(_hash_worker, raw_passwords))

        users_data = []
        for i in range(count):
            users_data.append({
                "username": f"real_user_{run_id}_{i}",
                "full_name": f"Real User {i}",
                "email": f"real_{run_id}_{i}@prod.com",
                "biography": "Unique hash generated via multiprocessing",
                "password": hashed_passwords[i]
            })

        stmt = insert(User).values(users_data)
        await self._session.execute(stmt)
        await self._session.commit()

        return len(users_data)