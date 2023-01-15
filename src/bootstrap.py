import asyncio
import concurrent.futures
import inspect

from src.adapters.repositories.aiosqlite.create_db import create_tables
from src.service_layer import handlers, messagebus
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork
from src.service_layer.unit_of_work.aiosqlite_unit_of_work import \
    AiosqliteUnitOfWork


def bootstrap(
    init_database_if_not_exists: bool = True,
    uow: AbstractUnitOfWork = AiosqliteUnitOfWork(),
) -> messagebus.MessageBus:

    if init_database_if_not_exists:
        pool = concurrent.futures.ThreadPoolExecutor()
        pool.submit(asyncio.run, create_tables())

    dependencies = {"uow": uow}
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
