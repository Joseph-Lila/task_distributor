import asyncio

from kivy.clock import Clock, mainthread

from src.entrypoints.kivy.views.main_screen.main_screen import MainScreenView
import asynckivy as ak


class MainScreenController:
    def __init__(self, bus):
        self.bus = bus
        self._view = MainScreenView(controller=self)
        Clock.schedule_once(self._init_manipulations, -1)

    def get_view(self):
        return self._view

    async def hard_operation(self):
        print('start')
        await ak.sleep(3)
        print('end')

    def _init_manipulations(self, *args):
        ak.start(self._view.do_with_loading_modal_view(self.hard_operation))
