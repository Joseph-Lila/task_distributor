import functools

from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
import asynckivy as ak


class MainScreenView(MDScreen):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loading_modal_view = Factory.LoadingModalView()

    async def do_with_loading_modal_view(self, func):
        self._open_loading_modal_view()
        await func()
        self._close_loading_modal_view()

    def _open_loading_modal_view(self):
        self._loading_modal_view.open()

    def _close_loading_modal_view(self):
        self._loading_modal_view.dismiss()
