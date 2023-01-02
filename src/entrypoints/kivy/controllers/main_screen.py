from src.entrypoints.kivy.views.main_screen.main_screen import MainScreenView


class MainScreenController:
    def __init__(self, bus):
        self.bus = bus
        self._view = MainScreenView(
            controller=self,
        )

    def get_view(self):
        return self._view
