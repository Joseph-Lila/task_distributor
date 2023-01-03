from kivy.clock import mainthread
import asynckivy as ak

from src.entrypoints.kivy.controllers.abstract_controller import AbstractController
from src.entrypoints.kivy.views.main_task_screen.main_task_screen import MainTaskScreenView


class MainTaskScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = MainTaskScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    @mainthread
    def _init_manipulations(self, *args):
        ak.start(self._view.update_negative_task())
        ak.start(self._view.update_current_task())
        ak.start(self._view.update_negative_tasks_quantity())
