from abc import ABC, abstractmethod
from api.pydantic.models import FolderUpdate, FolderResponse

class AbstractUpdateFolderUseCase(ABC):
    @abstractmethod
    async def execute(self, folder_id: int, payload: FolderUpdate) -> FolderResponse:
        ...