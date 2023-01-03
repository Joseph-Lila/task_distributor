import asyncio
import functools

from kivy.clock import mainthread
import asynckivy as ak

from src.domain.commands.get_all_tasks import GetAllTasks
from src.entrypoints.kivy.controllers.abstract_controller import AbstractController, use_bus
from src.entrypoints.kivy.views.tasks_log_screen.tasks_log_screen import TasksLogScreenView


class TasksLogScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = TasksLogScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    @use_bus
    async def get_all_tasks(self, *args):
        event = await self.bus.handle_command(GetAllTasks())
        if event:
            await self._view.update_data_table_rows(event.tasks)

    @mainthread
    def _init_manipulations(self, *args):
        ak.start(self.get_all_tasks())
