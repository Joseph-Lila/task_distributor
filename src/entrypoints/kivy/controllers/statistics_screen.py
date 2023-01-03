from kivy.clock import mainthread

from src.entrypoints.kivy.controllers.abstract_controller import AbstractController
from src.entrypoints.kivy.views.statistics_screen.statistics_screen import StatisticsScreenView


class StatisticsScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = StatisticsScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    @mainthread
    def _init_manipulations(self, *args):
        pass
