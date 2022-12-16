import abc

from src.adapters.repositories.sql_alchemy_repositories.common_task_repository import CommonTaskRepository


class AbstractUnitOfWork(abc.ABC):
    common_tasks: CommonTaskRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


