from api.pydantic.models import FolderUpdate, FolderResponse
from infrastructure.repositories.postgresql.folder.uow import PostgreSQLFolderUnitOfWork
from .abstract import AbstractUpdateFolderUseCase


class PostgreSQLUpdateFolderUseCase(AbstractUpdateFolderUseCase):
    def __init__(self, uow: PostgreSQLFolderUnitOfWork):
        self._uow = uow

    async def execute(self, folder_id: int, payload: FolderUpdate) -> FolderResponse:
        async with self._uow as uow:
            updated_folder = await uow.folder.update(folder_id, payload)
            await uow.commit()

            return FolderResponse.model_validate(updated_folder)