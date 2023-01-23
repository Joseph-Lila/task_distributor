import abc
from typing import List, Optional

from src.domain.entities.task import Task


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    async def get_all_tasks(self) -> List[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, task_id) -> Optional[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_tasks_by_type(self, status: str) -> List[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_task(
            self, title, deadline, period, description, estimation,
            status_title, register_title, task_type_title,
    ) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_task(self, task_id) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def edit_task(
            self, task_id, title, deadline, period,
            description, estimation, status_title,
            register_title, task_type_title,
            complexity_title
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_actual_task(self, current_task_place) -> Optional[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    async def change_task_status(self, task_id, status) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_task_type_id_by_task_type_title(self, task_type_title) -> Optional[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_register_id_by_register_title(self, register_title) -> Optional[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_status_id_by_status_title(self, status_title) -> Optional[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_complexity_id_by_complexity_title(self, complexity_title) -> Optional[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_task_py_place(self, place) -> Optional[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    async def change_place_and_complexity(self, task_id, place, complexity_title):
        raise NotImplementedError
