from typing import List, Optional

from dateutil.parser import parse

from src.adapters.repositories.abstract_repository import AbstractRepository
from src.domain.entities.complexity import Complexities
from src.domain.entities.task import Task
from src.domain.entities.unit import Unit


class AiosqliteRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    async def get_all_tasks(self) -> List[Task]:
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
            task_id = task_row[0]
            units = await self.get_task_units(task_id)
            tasks.append(
                Task(
                    item_id=task_row[0], title=task_row[1], deadline=parse(task_row[2]),
                    period=task_row[3], place=task_row[4], description=task_row[5],
                    estimation=task_row[6], status_title=task_row[7],
                    complexity_title=task_row[8], register_title=task_row[9],
                    task_type_title=task_row[10], units=units
                )
            )
        return tasks

    async def create_task(self, title, deadline, period, description, estimation, status_title, register_title,
                          task_type_title, complexity_title=Complexities.UNDEFINED.value) -> int:
        status_id = await self.get_status_id_by_status_title(status_title)
        register_id = await self.get_register_id_by_register_title(register_title)
        task_type_id = await self.get_task_type_id_by_task_type_title(task_type_title)
        complexity_id = await self.get_complexity_id_by_complexity_title(complexity_title)

        if not (status_id and register_id and task_type_id and complexity_id):
            raise ValueError('Cannot get id by title...')
        cursor = await self.session.cursor()
        await cursor.execute(
            "INSERT INTO tasks "
            "(title, deadline, period, description, estimation, status_id, complexity_id, register_id, task_type_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (title, deadline, period, description, estimation, status_id, complexity_id, register_id, task_type_id)
        )
        return cursor.lastrowid

    async def delete_task(self, task_id) -> None:
        await self.session.execute(
            "DELETE FROM tasks "
            "WHERE id = ?;",
            (task_id,)
        )

    async def edit_task(self, task_id, title, deadline, period, description, estimation, status_title, register_title,
                        task_type_title, complexity_title) -> None:
        status_id = await self.get_status_id_by_status_title(status_title)
        register_id = await self.get_register_id_by_register_title(register_title)
        task_type_id = await self.get_task_type_id_by_task_type_title(task_type_title)
        complexity_id = await self.get_complexity_id_by_complexity_title(complexity_title)
        await self.session.execute(
            "UPDATE tasks "
            "SET title = ?, deadline = ?, period = ?, description = ?, estimation = ?, status_id = ?, "
            "complexity_id = ?, register_id = ?, task_type_id = ? "
            "WHERE id = ?",
            (title, deadline, period, description, estimation, status_id, complexity_id, register_id, task_type_id,
             task_id)
        )

    async def get_task_py_place(self, place) -> Optional[Task]:
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
            "ON tasks.task_type_id = task_types.id "
            "WHERE tasks.place = ?;",
            (place,)
        )
        task_row = await cursor.fetchone()
        if task_row:
            task_id = task_row[0]
            units = await self.get_task_units(task_id)
            return Task(*task_row, units=units)

    async def get_actual_task(self, current_task_place=None) -> Optional[Task]:
        if current_task_place is None:
            needed_place = 1
        else:
            needed_place = current_task_place + 1
        task = await self.get_task_py_place(needed_place)
        if not task:
            needed_place = 1
            task = await self.get_task_py_place(needed_place)
        return task

    async def change_task_status(self, task_id, status) -> None:
        status_id = await self.get_status_id_by_status_title(status)
        await self.session.execute(
            "UPDATE tasks "
            "SET status_id = ? "
            "WHERE id = ?",
            (status_id, task_id)
        )

    async def get_status_id_by_status_title(self, status_title) -> Optional[int]:
        cursor = await self.session.execute(
            "SELECT id "
            "FROM statuses "
            "WHERE title = ?;",
            (status_title,)
        )
        status_id = await cursor.fetchone()

        if status_id:
            return status_id[0]

    async def get_register_id_by_register_title(self, register_title) -> Optional[int]:
        cursor = await self.session.execute(
            "SELECT id "
            "FROM registers "
            "WHERE title = ?;",
            (register_title,)
        )

        register_id = await cursor.fetchone()
        if register_id:
            return register_id[0]

    async def get_complexity_id_by_complexity_title(self, complexity_title) -> Optional[int]:
        cursor = await self.session.execute(
            "SELECT * "
            "FROM complexities "
            "WHERE title = ?;",
            (complexity_title,)
        )

        complexity_id = await cursor.fetchone()
        if complexity_id:
            return complexity_id[0]

    async def get_task_type_id_by_task_type_title(self, task_type_title) -> Optional[int]:
        cursor = await self.session.execute(
            "SELECT * "
            "FROM task_types "
            "WHERE title = ?;",
            (task_type_title,)
        )

        task_type_id = await cursor.fetchone()
        if task_type_id:
            return task_type_id[0]

    async def get_task_units(self, task_id) -> Optional[List[Unit]]:
        cursor = await self.session.execute(
            "SELECT * "
            "FROM units "
            "WHERE task_id = ?;",
            (task_id,)
        )
        task_unit_rows = await cursor.fetchall()
        if not task_unit_rows:
            return None
        task_units = []
        for task_unit_row in task_unit_rows:
            task_units.append(Unit(*task_unit_row))
        return task_units

    async def add_task_unit(self, estimation, status_title, task_id) -> None:
        status_id = await self.get_status_id_by_status_title(status_title)
        await self.session.execute(
            "INSERT INTO units "
            "(estimation, status_id, task_id) "
            "VALUES (?, ?, ?);",
            (estimation, status_id, task_id)
        )

    async def edit_task_unit(self, task_unit_id, estimation, status_title) -> None:
        status_id = await self.get_status_id_by_status_title(status_title)
        await self.session.execute(
            "UPDATE units "
            "SET estimation = ?, status_id = ? "
            "WHERE id = ?",
            (estimation, status_id, task_unit_id)
        )

    async def delete_task_unit(self, task_unit_id) -> None:
        await self.session.execute(
            "DELETE FROM units "
            "WHERE id = ?;",
            (task_unit_id,)
        )
