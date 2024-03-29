from src.entrypoints.kivy_gui.controllers.abstract_controller import \
    AbstractController
from src.entrypoints.kivy_gui.views.statistics_screen.statistics_screen import \
    StatisticsScreenView


class StatisticsScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = StatisticsScreenView(controller=self)

    def get_view(self):
        return self._view
