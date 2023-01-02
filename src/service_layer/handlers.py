from typing import Callable, Dict, Type

from src.domain.commands.command import Command
from src.domain.commands.create_task import CreateTask
from src.domain.events.task_is_created import TaskIsCreated
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


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
}  # type: Dict[Type[Command], Callable]
