from abc import ABC, abstractmethod
from typing import List
from api.pydantic.models import FolderResponse

class AbstractGetFoldersUseCase(ABC):
    @abstractmethod
    async def execute(self) -> List[FolderResponse]:
        ...