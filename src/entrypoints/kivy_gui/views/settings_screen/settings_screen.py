from kivy.properties import ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem


class SettingsScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()
