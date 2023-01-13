import asyncio
import datetime
import functools

from kivy.clock import mainthread
import asynckivy as ak

from src.domain.commands.create_task import CreateTask
from src.domain.commands.get_all_tasks import GetAllTasks
from src.domain.entities.task_type import TaskTypes
from src.entrypoints.kivy.controllers.abstract_controller import AbstractController, use_loop
from src.entrypoints.kivy.views.tasks_log_screen.tasks_log_screen import TasksLogScreenView


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
        event = await self.bus.handle_command(
            CreateTask(
                title, deadline, period, description, estimation,
                status_title, register_title, task_type_title
            )
        )
        if event:
            await self._view

    @mainthread
    def _init_manipulations(self, *args):
        ak.start(self.get_all_tasks())

    @staticmethod
    async def get_available_task_types():
        return [item.value for item in TaskTypes]

    def go_to_creation_screen(self, *args):
        self._view.screen_manager.current = 'add task'

    def go_to_table_screen(self, *args):
        self._view.screen_manager.current = 'table'
