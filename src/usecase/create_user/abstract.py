from abc import ABC, abstractmethod

from api.pydantic.models import CreateUserSchema, UserRead


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CreateUserSchema) -> UserRead:
        ...