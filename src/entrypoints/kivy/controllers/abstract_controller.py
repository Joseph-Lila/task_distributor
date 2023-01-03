import abc

from kivy.clock import mainthread


class AbstractController(abc.ABC):
    def __init__(self):
        self._init_manipulations()

    @mainthread
    def _init_manipulations(self, *args):
        raise NotImplementedError
