import datetime

import pytest

from src.adapters.repositories.aiosqlite.create_db import CREATE_CONSTRUCTIONS
from src.domain.entities.complexity import Complexities
from src.domain.entities.register import TASKS_DEFAULT_REGISTER
from src.domain.entities.status import Statuses
from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes
from src.service_layer.unit_of_work.aiosqlite_unit_of_work import AiosqliteUnitOfWork


@pytest.mark.asyncio
async def test_transaction(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        assert in_memory_sqlite_db == ':memory:'


@pytest.mark.asyncio
async def test_repository_get_task_type_id_by_task_type_title(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    task_type_title = 'COMMON'
    async with uow:
        # create tables
        for item in CREATE_CONSTRUCTIONS:
            await uow.conn.execute(item)
        await uow.commit()
        # add task_type elem
        await uow.conn.execute(
            "INSERT INTO task_types "
            "(title, description) "
            "VALUES (?, ?);",
            (task_type_title, '')
        )
        await uow.commit()

        task_type_id = await uow.repository.get_task_type_id_by_task_type_title(task_type_title)
        assert task_type_id == 1


@pytest.mark.asyncio
async def test_repository_get_register_id_by_register_title(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    register_title = TASKS_DEFAULT_REGISTER
    async with uow:
        # create tables
        for item in CREATE_CONSTRUCTIONS:
            await uow.conn.execute(item)
        await uow.commit()
        # add task_type elem
        await uow.conn.execute(
            "INSERT INTO registers "
            "(title, description) "
            "VALUES (?, ?);",
            (register_title, '')
        )
        await uow.commit()

        register_id = await uow.repository.get_register_id_by_register_title(register_title)
        assert register_id == 1


@pytest.mark.asyncio
async def test_repository_get_status_id_by_status_title(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    status_title = 'DONE'
    async with uow:
        # create tables
        for item in CREATE_CONSTRUCTIONS:
            await uow.conn.execute(item)
        await uow.commit()
        # add task_type elem
        await uow.conn.execute(
            "INSERT INTO statuses "
            "(title, description) "
            "VALUES (?, ?);",
            (status_title, '')
        )
        await uow.commit()

        task_type_id = await uow.repository.get_status_id_by_status_title(status_title)
        assert task_type_id == 1


@pytest.mark.asyncio
async def test_repository_get_complexity_id_by_complexity_title(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    complexity_title = 'EASY'
    async with uow:
        # create tables
        for item in CREATE_CONSTRUCTIONS:
            await uow.conn.execute(item)
        await uow.commit()
        # add task_type elem
        await uow.conn.execute(
            "INSERT INTO complexities "
            "(title, description) "
            "VALUES (?, ?);",
            (complexity_title, '')
        )
        await uow.commit()

        complexity_id = await uow.repository.get_complexity_id_by_complexity_title(complexity_title)
        assert complexity_id == 2


@pytest.mark.asyncio
async def test_create_task_and_get_tasks(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    status_title = Statuses.IN_PROGRESS.value
    register_title = 'TASKS'
    task_type_title = TaskTypes.COMMON.value
    complexity_title = 'UNDEFINED'
    title = 'Task1'
    deadline = datetime.datetime.now()
    period = 60
    description = ''
    estimation = 45
    async with uow:
        # create tables
        for item in CREATE_CONSTRUCTIONS:
            await uow.conn.execute(item)
        await uow.commit()
        await uow.conn.execute(
            "INSERT INTO statuses "
            "(title, description) "
            "VALUES (?, ?);",
            (status_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO complexities "
            "(title, description) "
            "VALUES (?, ?);",
            (complexity_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO registers "
            "(title, description) "
            "VALUES (?, ?);",
            (register_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO task_types "
            "(title, description) "
            "VALUES (?, ?);",
            (task_type_title, '')
        )
        await uow.commit()
        await uow.repository.create_task(title, deadline, period, description, estimation, status_title, register_title,
                                         task_type_title)
        await uow.commit()
        tasks = await uow.repository.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0] == Task(
            item_id=1, title=title, deadline=deadline, period=period,
            place=None, description=description, estimation=estimation,
            status_title=status_title, complexity_title=complexity_title,
            register_title=register_title, task_type_title=task_type_title
        )


@pytest.mark.asyncio
async def test_delete_task_and_get_tasks(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    status_title = Statuses.IN_PROGRESS.value
    register_title = 'TASKS'
    task_type_title = TaskTypes.COMMON.value
    complexity_title = 'UNDEFINED'
    title = 'Task1'
    deadline = datetime.datetime.now()
    period = 60
    description = ''
    estimation = 45
    async with uow:
        # create tables
        for item in CREATE_CONSTRUCTIONS:
            await uow.conn.execute(item)
        await uow.commit()
        await uow.conn.execute(
            "INSERT INTO statuses "
            "(title, description) "
            "VALUES (?, ?);",
            (status_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO complexities "
            "(title, description) "
            "VALUES (?, ?);",
            (complexity_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO registers "
            "(title, description) "
            "VALUES (?, ?);",
            (register_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO task_types "
            "(title, description) "
            "VALUES (?, ?);",
            (task_type_title, '')
        )
        await uow.commit()
        await uow.repository.create_task(title, deadline, period, description, estimation, status_title, register_title,
                                         task_type_title)
        await uow.commit()

        tasks = await uow.repository.get_all_tasks()
        assert len(tasks) == 1
        await uow.repository.delete_task(1)
        tasks = await uow.repository.get_all_tasks()
        assert len(tasks) == 0


@pytest.mark.asyncio
async def test_edit_task(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    status_title = Statuses.IN_PROGRESS.value
    register_title = 'TASKS'
    task_type_title = TaskTypes.COMMON.value
    complexity_title = Complexities.UNDEFINED.value
    title = 'Task1'
    new_title = 'New Task 1'
    deadline = datetime.datetime.now()
    period = 60
    description = ''
    estimation = 45
    async with uow:
        # create tables
        for item in CREATE_CONSTRUCTIONS:
            await uow.conn.execute(item)
        await uow.commit()
        await uow.conn.execute(
            "INSERT INTO statuses "
            "(title, description) "
            "VALUES (?, ?);",
            (status_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO complexities "
            "(title, description) "
            "VALUES (?, ?);",
            (complexity_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO registers "
            "(title, description) "
            "VALUES (?, ?);",
            (register_title, '')
        )
        await uow.conn.execute(
            "INSERT INTO task_types "
            "(title, description) "
            "VALUES (?, ?);",
            (task_type_title, '')
        )
        await uow.commit()
        await uow.repository.create_task(title, deadline, period, description, estimation, status_title, register_title,
                                         task_type_title)
        await uow.commit()
        tasks = await uow.repository.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0] == Task(
            item_id=1, title=title, deadline=deadline, period=period,
            place=None, description=description, estimation=estimation,
            status_title=status_title, complexity_title=complexity_title,
            register_title=register_title, task_type_title=task_type_title,
        )
        await uow.repository.edit_task(
            1, new_title, deadline, period, description, estimation, status_title,
            register_title, task_type_title, complexity_title)
        tasks = await uow.repository.get_all_tasks()
        assert tasks[0] == Task(
            item_id=1, title=new_title, deadline=deadline, period=period,
            place=None, description=description, estimation=estimation,
            status_title=status_title, complexity_title=complexity_title,
            register_title=register_title, task_type_title=task_type_title,
        )

