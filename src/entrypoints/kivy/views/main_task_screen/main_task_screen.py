from kivy.properties import ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem


class MainTaskScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()
