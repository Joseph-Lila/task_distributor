import abc
from typing import List

from src.domain.entities.base_task import BaseTask


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_next_task(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_statistics(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tasks_by_type(self, task_type: str) -> List[BaseTask]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, task_id: int) -> bool:
        raise NotImplementedError
