import abc


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    async def get_tasks(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def create_task(
            self, title, deadline, period, description, estimation,
            status_title, register_title, task_type_title,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_task(self, task_id):
        raise NotImplementedError

    @abc.abstractmethod
    async def edit_task(
            self, task_id, title, deadline, period,
            description, estimation, status_title,
            register_title, task_type_title,
            complexity_title
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_actual_task(self, current_task_place):
        raise NotImplementedError

    @abc.abstractmethod
    async def change_task_status(self, task_id, status):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_task_type_id_by_task_type_title(self, task_type_title):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_register_id_by_register_title(self, register_title):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_status_id_by_status_title(self, status_title):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_complexity_id_by_complexity_title(self, complexity_title):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_task_units(self, task_id):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_task_unit(self, estimation, status_title, task_id):
        raise NotImplementedError

    @abc.abstractmethod
    async def edit_task_unit(self, task_unit_id, estimation, status_title):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_task_unit(self, task_unit_id):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_task_py_place(self, place):
        raise NotImplementedError
