from abc import ABC, abstractmethod
from api.pydantic.models import ThemeCreate, ThemeResponse

class AbstractCreateThemeUseCase(ABC):
    @abstractmethod
    async def execute(self, folder_id: int, schema: ThemeCreate, user_id: int) -> ThemeResponse:
        ...