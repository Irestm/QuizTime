from abc import ABC, abstractmethod

class AbstractDeleteThemeUseCase(ABC):
    @abstractmethod
    async def execute(self, theme_id: int, user_id: int) -> None:
        ...