from typing import Callable, Dict, Type

from src.domain.commands.command import Command
from src.domain.commands.create_task import CreateTask
from src.domain.commands.get_all_tasks import GetAllTasks
from src.domain.events.got_all_tasks import GotAllTasks
from src.domain.events.task_is_created import TaskIsCreated
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


async def get_all_tasks(
        cmd: GetAllTasks,
        uow: AbstractUnitOfWork,
):
    async with uow:
        tasks = await uow.repository.get_all_tasks()
    return GotAllTasks(tasks)


async def create_task(
        cmd: CreateTask,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.create_task(
            cmd.title, cmd.deadline, cmd.period,
            cmd.description, cmd.estimation,
            cmd.status_title, cmd.register_title,
            cmd.task_type_title
        )
        await uow.commit()
    return TaskIsCreated(cmd.title, cmd.deadline, cmd.period,
                         cmd.description, cmd.estimation,
                         cmd.status_title, cmd.register_title,
                         cmd.task_type_title)


COMMAND_HANDLERS = {
    CreateTask: create_task,
    GetAllTasks: get_all_tasks,
}  # type: Dict[Type[Command], Callable]
