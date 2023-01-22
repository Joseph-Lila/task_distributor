import asynckivy as ak
from kivy.clock import mainthread

from src.domain.commands.allocate_tasks import AllocateTasks
from src.domain.commands.get_main_task import GetMainTask
from src.domain.commands.mark_task_as_done import MarkTaskAsDone
from src.domain.commands.mark_task_as_frozen import MarkTaskAsFrozen
from src.domain.events.got_main_task import GotMainTask
from src.domain.events.tasks_are_allocated import TasksAreAllocated
from src.entrypoints.kivy.controllers.abstract_controller import (
    AbstractController, use_loop)
from src.entrypoints.kivy.views.main_task_screen.main_task_screen import \
    MainTaskScreenView


class MainTaskScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = MainTaskScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    @use_loop
    async def get_main_task(self, current_task_place=None):
        await self.bus.handle_command(
            AllocateTasks()
        )
        event: GotMainTask = await self.bus.handle_command(GetMainTask(current_task_place))
        await self._view.update_current_task(event.task)

    @use_loop
    async def mark_task_as_done(self, task_id: int):
        await self.bus.handle_command(
            MarkTaskAsDone(task_id)
        )
        await self.get_main_task()

    @use_loop
    async def mark_task_as_frozen(self, task_id: int):
        await self.bus.handle_command(
            MarkTaskAsFrozen(task_id)
        )
        await self.get_main_task()

    @mainthread
    def _init_manipulations(self, *args):
        ak.start(self._view.update_negative_task())
        ak.start(self._view.update_negative_tasks_quantity())
