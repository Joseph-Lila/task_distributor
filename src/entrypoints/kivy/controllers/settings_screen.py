from kivy.clock import mainthread

from src.entrypoints.kivy.controllers.abstract_controller import AbstractController
from src.entrypoints.kivy.views.settings_screen.settings_screen import SettingsScreenView


class SettingsScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = SettingsScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    @mainthread
    def _init_manipulations(self, *args):
        pass
