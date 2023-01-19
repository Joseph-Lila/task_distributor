from typing import Callable, Dict, Type

from loguru import logger

from src.domain.commands.allocate_tasks import AllocateTasks
from src.domain.commands.command import Command
from src.domain.commands.create_task import CreateTask
from src.domain.commands.create_task_unit import CreateTaskUnit
from src.domain.commands.edit_task import EditTask
from src.domain.commands.edit_task_unit import EditTaskUnit
from src.domain.commands.get_all_tasks import GetAllTasks
from src.domain.commands.get_tasks_by_type import GetTasksByType
from src.domain.events.got_all_tasks import GotAllTasks
from src.domain.events.task_is_created import TaskIsCreated
from src.domain.events.task_is_edited import TaskIsEdited
from src.domain.events.tasks_are_allocated import TasksAreAllocated
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


async def get_all_tasks(
        cmd: GetAllTasks,
        uow: AbstractUnitOfWork,
):
    async with uow:
        tasks = await uow.repository.get_all_tasks()
    return GotAllTasks(tasks)


async def get_tasks_by_type(
        cmd: GetTasksByType,
        uow: AbstractUnitOfWork,
):
    async with uow:
        tasks = await uow.repository.get_tasks_by_type(cmd.status_title)
    return GotAllTasks(tasks)


async def create_task(
        cmd: CreateTask,
        uow: AbstractUnitOfWork,
):
    async with uow:
        new_item_id = await uow.repository.create_task(
            cmd.title, cmd.deadline, cmd.period,
            cmd.description, cmd.estimation,
            cmd.status_title, cmd.register_title,
            cmd.task_type_title,
        )
        await uow.commit()
    return TaskIsCreated(new_item_id)


async def create_task_unit(
        cmd: CreateTaskUnit,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.create_task_unit(
            cmd.estimation,
            cmd.status_title,
            cmd.task_id,
        )
        await uow.commit()


async def edit_task(
        cmd: EditTask,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.edit_task(
            task_id=cmd.task_id,
            title=cmd.title,
            deadline=cmd.deadline,
            period=cmd.period,
            description=cmd.description,
            estimation=cmd.estimation,
            status_title=cmd.status_title,
            register_title=cmd.register_title,
            task_type_title=cmd.task_type_title,
            complexity_title=cmd.complexity_title,
        )
        await uow.commit()
    return TaskIsEdited(cmd.task_id)


async def edit_task_unit(
        cmd: EditTaskUnit,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.edit_task_unit(
            task_unit_id=cmd.task_unit_id,
            estimation=cmd.estimation,
            status_title=cmd.status_title,
        )
        await uow.commit()


async def allocate_tasks(
        cmd: AllocateTasks,
        uow: AbstractUnitOfWork,
):
    return TasksAreAllocated()


COMMAND_HANDLERS = {
    CreateTask: create_task,
    GetAllTasks: get_all_tasks,
    GetTasksByType: get_tasks_by_type,
    CreateTaskUnit: create_task_unit,
    AllocateTasks: allocate_tasks,
    EditTask: edit_task,
    EditTaskUnit: edit_task_unit,
}  # type: Dict[Type[Command], Callable]
