import asynckivy as ak
from kivy.clock import mainthread

from src.domain.commands.get_main_task import GetMainTask
from src.domain.events.got_main_task import GotMainTask
from src.entrypoints.kivy.controllers.abstract_controller import \
    AbstractController, use_loop
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
        event: GotMainTask = await self.bus.handle_command(GetMainTask(current_task_place))
        if event:
            await self._view.update_current_task(event.task)

    @mainthread
    def _init_manipulations(self, *args):
        ak.start(self._view.update_negative_task())
        ak.start(self.get_main_task())
        ak.start(self._view.update_negative_tasks_quantity())
