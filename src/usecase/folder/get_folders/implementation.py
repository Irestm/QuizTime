from typing import List
from api.pydantic.models import FolderResponse, Pagination
from infrastructure.repositories.postgresql.folder.uow import PostgreSQLFolderUnitOfWork
from .abstract import AbstractGetFoldersUseCase

class PostgreSQLGetFoldersUseCase(AbstractGetFoldersUseCase):
    def __init__(self, uow: PostgreSQLFolderUnitOfWork):
        self._uow = uow

    async def execute(self, pagination: Pagination) -> List[FolderResponse]:
        async with self._uow as uow:
            folders = await uow.folder.get_all(pagination)
            return [FolderResponse.model_validate(f) for f in folders]