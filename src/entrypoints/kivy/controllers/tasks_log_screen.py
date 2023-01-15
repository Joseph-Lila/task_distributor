import asyncio
import datetime
import functools

import asynckivy as ak
from kivy.clock import mainthread

from src.domain.commands.create_task import CreateTask
from src.domain.commands.get_all_tasks import GetAllTasks
from src.domain.entities.complexity import Complexities
from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes
from src.domain.events.task_is_created import TaskIsCreated
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
    async def create_task(
            self, title: str, deadline: datetime.datetime, period: int,
            description: str, estimation: int, status_title: str,
            register_title: str, task_type_title: str):
        event: TaskIsCreated = await self.bus.handle_command(
            CreateTask(
                title, deadline, period, description, estimation,
                status_title, register_title, task_type_title
            )
        )
        if event:
            new_task = Task(
                item_id=event.id,
                title=event.title,
                deadline=event.deadline,
                period=event.period,
                place=None,
                description=event.description,
                estimation=event.estimation,
                status_title=event.status_title,
                complexity_title=Complexities.UNDEFINED.value,
                register_title=event.register_title,
                task_type_title=event.task_type_title,
                units=None,
            )
            await self._view.append_data_table_row(new_task)

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
