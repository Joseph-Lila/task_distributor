import asyncio
import datetime
import functools
from typing import Optional, List

import asynckivy as ak
from kivy.clock import mainthread

from src.domain.commands.allocate_tasks import AllocateTasks
from src.domain.commands.create_task import CreateTask
from src.domain.commands.create_task_unit import CreateTaskUnit
from src.domain.commands.get_all_tasks import GetAllTasks
from src.domain.commands.get_tasks_by_type import GetTasksByType
from src.domain.entities.complexity import Complexities
from src.domain.entities.status import Statuses
from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes
from src.domain.entities.unit import Unit
from src.domain.events.task_is_created import TaskIsCreated
from src.domain.events.tasks_are_allocated import TasksAreAllocated
from src.entrypoints.kivy.controllers.abstract_controller import (
    AbstractController, use_loop)
from src.entrypoints.kivy.views.tasks_log_screen.tasks_log_screen import \
    TasksLogScreenView


class TasksLogScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = TasksLogScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    @use_loop
    async def get_all_tasks(self):
        event = await self.bus.handle_command(GetAllTasks())
        if event:
            await self._view.update_data_table_rows(event.tasks)

    @use_loop
    async def get_tasks_by_type(self, status: str):
        event = await self.bus.handle_command(GetTasksByType(status))
        if event:
            await self._view.update_data_table_rows(event.tasks)

    @use_loop
    async def create_task(
            self, title: str, deadline: datetime.datetime, period: int,
            description: str, estimation: int, status_title: str,
            register_title: str, task_type_title: str, units: Optional[List[Unit]]):
        # crate task
        event: TaskIsCreated = await self.bus.handle_command(
            CreateTask(
                title, deadline, period, description, estimation,
                status_title, register_title, task_type_title
            )
        )
        # create units for it if needed
        if event and units:
            for unit in units:
                await self.bus.handle_command(
                    CreateTaskUnit(
                        estimation=unit.estimation,
                        status_title=Statuses.IN_PROGRESS.value,
                        task_id=event.id
                    )
                )
        # allocate tasks
        event: TasksAreAllocated = await self.bus.handle_command(
            AllocateTasks()
        )
        # update data table
        if event:
            self._view.update_table()

    @mainthread
    def _init_manipulations(self, *args):
        pass

    @staticmethod
    async def get_available_task_types():
        return [item.value for item in TaskTypes]

    def go_to_creation_screen(self, *args):
        self._view.task_log_screen_manager.current = 'tasks fields screen'

    def go_to_table_screen(self, *args):
        self._view.task_log_screen_manager.current = 'table'

    def go_to_units_screen(self, *args):
        self._view.task_log_screen_manager.current = 'units screen'
