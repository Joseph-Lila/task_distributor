from src.entrypoints.kivy.views.statistics_screen.statistics_screen import StatisticsScreenView


class StatisticsScreenController:
    def __init__(self, bus):
        self.bus = bus
        self._view = StatisticsScreenView(
            controller=self,
        )

    def get_view(self):
        return self._view
