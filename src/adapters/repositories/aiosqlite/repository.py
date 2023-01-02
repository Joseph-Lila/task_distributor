from src.adapters.repositories.abstract_repository import AbstractRepository
from src.domain.entities.complexity import Complexities
from src.domain.entities.task import Task


class AiosqliteRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    async def get_tasks(self):
        cursor = await self.session.execute(
            "SELECT tasks.id, tasks.title, tasks.deadline, tasks.period, tasks.place, tasks.description, "
            "tasks.estimation, statuses.title, complexities.title, registers.title, task_types.title "
            "FROM tasks INNER JOIN statuses "
            "ON tasks.status_id = statuses.id "
            "INNER JOIN complexities "
            "ON tasks.complexity_id = complexities.id "
            "INNER JOIN registers "
            "ON tasks.register_id = registers.id "
            "INNER JOIN task_types "
            "ON tasks.task_type_id = task_types.id;"
        )
        task_rows = await cursor.fetchall()
        tasks = []
        for task_row in task_rows:
            tasks.append(Task(*task_row, units=None))
        return tasks

    async def create_task(self, title, deadline, period, description, estimation, status_title, register_title,
                          task_type_title, complexity_title=Complexities.UNDEFINED.value):
        status_id = await self.get_status_id_by_status_title(status_title)
        register_id = await self.get_register_id_by_register_title(register_title)
        task_type_id = await self.get_task_type_id_by_task_type_title(task_type_title)
        complexity_id = await self.get_complexity_id_by_complexity_title(complexity_title)
        await self.session.execute(
            "INSERT INTO tasks "
            "(title, deadline, period, description, estimation, status_id, complexity_id, register_id, task_type_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (title, deadline, period, description, estimation, status_id, complexity_id, register_id, task_type_id)
        )

    async def delete_task(self, task_id):
        pass

    async def edit_task(self, task_id, title, deadline, period, description, estimation, status_title, register_title,
                        task_type_title):
        pass

    async def get_another_task(self, current_task_place):
        pass

    async def get_main_task(self):
        pass

    async def mark_task_as_done(self, task_id):
        pass

    async def get_status_id_by_status_title(self, status_title):
        cursor = await self.session.execute(
            "SELECT id "
            "FROM statuses "
            "WHERE title = ?;",
            (status_title,)
        )
        status_id = await cursor.fetchone()
        return status_id[0]

    async def get_register_id_by_register_title(self, register_title):
        cursor = await self.session.execute(
            "SELECT id "
            "FROM registers "
            "WHERE title = ?;",
            (register_title,)
        )
        register_id = await cursor.fetchone()
        return register_id[0]

    async def get_complexity_id_by_complexity_title(self, complexity_title):
        cursor = await self.session.execute(
            "SELECT * "
            "FROM complexities "
            "WHERE title = ?;",
            (complexity_title,)
        )
        complexity_id = await cursor.fetchone()
        return complexity_id[0]

    async def get_task_type_id_by_task_type_title(self, task_type_title):
        cursor = await self.session.execute(
            "SELECT * "
            "FROM task_types "
            "WHERE title = ?;",
            (task_type_title,)
        )
        task_type_id = await cursor.fetchone()
        return task_type_id[0]
