from src.entrypoints.kivy.views.main_task_screen.main_task_screen import MainTaskScreenView


class MainTaskScreenController:
    def __init__(self, bus):
        self.bus = bus
        self._view = MainTaskScreenView(
            controller=self,
        )

    def get_view(self):
        return self._view
