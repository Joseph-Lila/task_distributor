from src.entrypoints.kivy.views.tasks_log_screen.tasks_log_screen import TasksLogScreenView


class TasksLogScreenController:
    def __init__(self, bus):
        self.bus = bus
        self._view = TasksLogScreenView(
            controller=self,
        )

    def get_view(self):
        return self._view
