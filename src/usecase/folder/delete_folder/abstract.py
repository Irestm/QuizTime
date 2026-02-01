from abc import ABC, abstractmethod

class AbstractDeleteFolderUseCase(ABC):
    @abstractmethod
    async def execute(self, folder_id: int) -> None:
        ...