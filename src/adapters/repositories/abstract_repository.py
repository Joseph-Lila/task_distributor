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
            register_title, task_type_title
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_another_task(self, current_task_place):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_main_task(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def mark_task_as_done(self, task_id):
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
