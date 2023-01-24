import asyncio

from kivy.utils import platform


if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions(
        [
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ]
    )

from kivymd.app import MDApp
from src.entrypoints.kivy_gui.screens import ScreenGenerator


class KivyApp(MDApp):
    title = 'Task Distributor'
    icon = 'assets/images/icon.jpg'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from src.entrypoints.kivy_gui.views.main import DateField, MyTextField
        self.load_all_kv_files(self.directory)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.material_style = "M3"
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    asyncio.run(KivyApp().async_run(async_lib='asyncio'))
