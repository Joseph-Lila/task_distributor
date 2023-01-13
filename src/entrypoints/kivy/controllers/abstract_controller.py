import abc
import asyncio
import functools

from kivy.clock import mainthread
from kivy.factory import Factory


async def do_with_loading_modal_view(func, *args, **kwargs):
    loading_modal_view = Factory.LoadingModalView()
    loading_modal_view.open()
    await func(*args, **kwargs)
    loading_modal_view.dismiss()


def use_loop(func):
    @functools.wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(func(self, *args, **kwargs))

    return wrapped


class AbstractController(abc.ABC):
    def __init__(self):
        self._init_manipulations()

    @mainthread
    def _init_manipulations(self, *args):
        raise NotImplementedError
