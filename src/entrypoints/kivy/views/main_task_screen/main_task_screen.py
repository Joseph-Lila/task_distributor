from kivy.properties import ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.taptargetview import MDTapTargetView


class MainTaskScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tap_target_view = None
        self._init_view()

    def _init_view(self):
        self.tap_target_view = MDTapTargetView(
            widget=self.more_button,
            title_text='Title (main)',
            title_text_size="36sp",
            title_text_color=(204/255, 191/255, 0, 1),
            description_text='description',
            description_text_color=(0, 141/255, 142/255, 1),
            widget_position='bottom',
            outer_circle_color=(1, 1, 1)
        )

    def tap_target_start(self):
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()
