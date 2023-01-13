from kivy.clock import mainthread

from src.entrypoints.kivy.controllers.abstract_controller import AbstractController, do_with_loading_modal_view
from src.entrypoints.kivy.views.main_screen.main_screen import MainScreenView
import asynckivy as ak


class MainScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = MainScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    async def hard_operation(self, *args, **kwargs):
        print('start')
        # await ak.sleep(3)
        print('end')

    @mainthread
    def _init_manipulations(self, *args):
        ak.start(do_with_loading_modal_view(self.hard_operation, self))
