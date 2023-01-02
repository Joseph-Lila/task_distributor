from src.entrypoints.kivy.views.main_task_screen.main_task_screen import MainTaskScreenView


class MainTaskScreenController:
    def __init__(self, bus):
        self.bus = bus
        self._view = MainTaskScreenView(controller=self)
        self._init_manipulations()

    def get_view(self):
        return self._view

    def _init_manipulations(self):
        self._view.update_current_task()
        self._view.update_negative_task()
        self._view.update_negative_tasks_quantity()
