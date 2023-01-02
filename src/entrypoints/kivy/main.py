from kivy.core.window import Window

Window.size = (400, 600)

import asyncio

from kivymd.app import MDApp

from src.entrypoints.kivy.screens import ScreenGenerator


class KivyApp(MDApp):
    title = 'Task Distributor'
    icon = 'images/icon.jpeg'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "200"
        self.theme_cls.material_style = "M3"
        return ScreenGenerator().build_app_view()


if __name__ == '__main__':
    asyncio.run(KivyApp().async_run(async_lib='asyncio'))
