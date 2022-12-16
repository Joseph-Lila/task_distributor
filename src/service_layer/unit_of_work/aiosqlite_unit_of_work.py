""" Module src.unit_of_work """
import aiosqlite

from src import config
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


class AiosqliteUnitOfWork(AbstractUnitOfWork):
    """
    Class for transactions using aiosqlite
    """

    def __init__(self, connection_string=config.get_sqlite_connection_str()):
        super().__init__()
        self._connection_string = connection_string
        self._db = None

    async def __aenter__(self):
        self._db = await aiosqlite.connect(self._connection_string)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(self, *args)
        await self._db.close()

    async def _commit(self):
        await self._db.commit()

    async def rollback(self):
        """
        Method to rollback changes
        :return: None
        """
        await self._db.rollback()
