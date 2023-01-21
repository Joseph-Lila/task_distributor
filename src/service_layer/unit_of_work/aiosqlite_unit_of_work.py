""" Module src.unit_of_work """
import asyncio

import aiosqlite

from src import config
from src.adapters.repositories.aiosqlite.repository import AiosqliteRepository
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


class AiosqliteUnitOfWork(AbstractUnitOfWork):
    """
    Class for transactions using aiosqlite
    """

    def __init__(self, connection_string=config.get_sqlite_connection_str()):
        super().__init__()
        self._connection_string = connection_string
        self._connections = {}

    @property
    def conn(self):
        """
        Readonly property to get connection.
        :return:
        """
        return self._connections[asyncio.current_task().get_name()]

    async def __aenter__(self):
        self._connections[asyncio.current_task().get_name()] = \
            await aiosqlite.connect(self._connection_string)
        self.repository = AiosqliteRepository(self.conn)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(self, *args)
        await self.conn.close()
        self._connections.pop(asyncio.current_task().get_name())

    async def _commit(self):
        await self.conn.commit()

    async def rollback(self):
        """
        Method to rollback changes
        :return: None
        """
        await self.conn.rollback()
