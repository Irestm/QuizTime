from api.pydantic.models import FolderCreate, FolderResponse
from infrastructure.repositories.postgresql.folder.uow import PostgreSQLFolderUnitOfWork
from .abstract import AbstractCreateFolderUseCase


class PostgreSQLCreateFolderUseCase(AbstractCreateFolderUseCase):
    def __init__(self, uow: PostgreSQLFolderUnitOfWork):
        self._uow = uow

    async def execute(self, folder: FolderCreate, user_id: int) -> FolderResponse:
        async with self._uow as uow:
            new_folder = await uow.folder.create(folder, user_id)
            response = FolderResponse.model_validate(new_folder)
            await uow.commit()
            return response