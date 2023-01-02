from src.entrypoints.kivy.views.settings_screen.settings_screen import SettingsScreenView


class SettingsScreenController:
    def __init__(self, bus):
        self.bus = bus
        self._view = SettingsScreenView(
            controller=self,
        )

    def get_view(self):
        return self._view
