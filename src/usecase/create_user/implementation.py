from api.pydantic.models import CreateUserSchema
from .abstract import AbstractCreateUserUseCase
from infrastructure.security.password import get_password_hash

class PostgreSQLCreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CreateUserSchema):
        schema.password = get_password_hash(schema.password)

        async with self._uow as uow_:
            author = await uow_.repository.create(schema)

        return author
