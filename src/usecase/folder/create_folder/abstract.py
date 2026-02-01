from abc import ABC, abstractmethod
from api.pydantic.models import FolderCreate, FolderResponse

class AbstractCreateFolderUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: FolderCreate) -> FolderResponse:
        ...