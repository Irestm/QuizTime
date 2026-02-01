from abc import ABC, abstractmethod
from api.pydantic.models import ThemeResponse

class AbstractGetThemeUseCase(ABC):
    @abstractmethod
    async def execute(self, theme_id: int, user_id: int) -> ThemeResponse:
        ...