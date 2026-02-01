from abc import ABC, abstractmethod

from api.pydantic.models import UserLoginSchema

class AbstractCreateTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: UserLoginSchema):
        ...
