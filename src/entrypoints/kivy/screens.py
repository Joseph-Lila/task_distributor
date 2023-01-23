from src.bootstrap import bootstrap
from src.entrypoints.kivy.controllers.main_screen import MainScreenController
from src.entrypoints.kivy.controllers.main_task_screen import \
    MainTaskScreenController
from src.entrypoints.kivy.controllers.tasks_log_screen import \
    TasksLogScreenController

SCREENS = {
    "main screen": MainScreenController,
    "main task screen": MainTaskScreenController,
    "tasks log screen": TasksLogScreenController,
    # "statistics screen": StatisticsScreenController,
    # "settings screen": SettingsScreenController,
}


class ScreenGenerator:
    def __init__(self, screens=SCREENS):
        self.screens = screens
        self.bus = bootstrap()
        self._main_screen_key = 'main screen'

    def build_app_view(self):
        app_view = self._generate_view(self._main_screen_key)
        for key in self.screens.keys():
            if key != self._main_screen_key:
                view = self._generate_view(key)
                app_view.nav_btm.add_widget(view)
        return app_view

    def _generate_view(self, key):
        controller = self.screens[key](self.bus)
        view = controller.get_view()
        view.name = key
        return view
