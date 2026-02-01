from infrastructure.repositories.postgresql.folder.uow import PostgreSQLFolderUnitOfWork
from .abstract import AbstractDeleteFolderUseCase

class PostgreSQLDeleteFolderUseCase(AbstractDeleteFolderUseCase):
    def __init__(self, uow: PostgreSQLFolderUnitOfWork):
        self._uow = uow

    async def execute(self, folder_id: int) -> None:
        async with self._uow as uow:
            await uow.folder.delete(folder_id)
            await uow.commit()