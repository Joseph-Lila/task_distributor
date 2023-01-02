""" Module src.unit_of_work """
import abc
from typing import Optional

from src.adapters.repositories.abstract_repository import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    """
    Abstract class for `unit of work` realizations.
    """
    repository: Optional[AbstractRepository]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        """
        Method to confirm changes
        :return:
        """
        await self._commit()

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        """
        Method to rollback changes
        :return:
        """
        raise NotImplementedError
