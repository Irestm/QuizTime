from abc import ABC, abstractmethod
from api.pydantic.models import ThemeUpdate, ThemeResponse

class AbstractUpdateThemeUseCase(ABC):
    @abstractmethod
    async def execute(self, theme_id: int, schema: ThemeUpdate, user_id: int) -> ThemeResponse:
        ...