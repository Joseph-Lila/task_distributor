from kivy.properties import ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem


class TasksLogScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()
