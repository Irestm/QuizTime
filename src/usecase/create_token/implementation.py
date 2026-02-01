from api.pydantic.models import UserLoginSchema, Token
from infrastructure.security.password import verify_password
from infrastructure.security.token import create_access_token


class PostgreSQLCreateTokenUseCase:
    def __init__(self, uow):
        self.uow = uow

    async def execute(self, user_data: UserLoginSchema) -> Token | None:
        async with self.uow:
            user = await self.uow.repository.get_user_by_username(user_data.username)

            if not user:
                return None

            if not verify_password(user_data.password, user.password):
                return None

            access_token = create_access_token(data={"sub": user.username})

            return Token(access_token=access_token, token_type="bearer")