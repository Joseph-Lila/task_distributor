from src.entrypoints.kivy_gui.controllers.abstract_controller import (
    AbstractController)
from src.entrypoints.kivy_gui.views.main_screen.main_screen import MainScreenView


class MainScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = MainScreenView(controller=self)

    def get_view(self):
        return self._view
