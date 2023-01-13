import datetime
from functools import partial
from typing import List
import asynckivy as ak
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.menu import MDDropdownMenu
import asyncio

from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField

from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes
from src.entrypoints.kivy.controllers.abstract_controller import use_loop


class TasksLogScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_table = None
        self.task_types_menu = None
        self.date_dialog = None
        self.adding_dialog = None
        self._tasks: List[Task] = []
        self._init_view()

    def _init_view(self):
        ak.start(self._init_date_dialog())
        ak.start(self._add_data_table())
        ak.start(self._add_drop_down())
        ak.start(self._init_adding_dialog())

    async def _add_data_table(self):
        self._data_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("Title", dp(45)),
                ("Deadline", dp(45)),
                ("Period", dp(30)),
                ("Status", dp(35)),
                ("Type", dp(35)),
            ],
            row_data=[],
            elevation=2,
        )
        self.data_table_cont.add_widget(self._data_table)

    async def _init_date_dialog(self):
        self.date_dialog = MDDatePicker(
            min_date=datetime.date.today(),
        )
        self.date_dialog.bind(on_save=self.on_save_date_dialog)

    def on_save_date_dialog(self, instance, value, date_range):
        self.adding_dialog.content_cls.date_field.text = str(value)

    async def generate_units(self, *args):
        units_quantity = self.adding_dialog.content_cls.panel.content.units_quantity.text
        if units_quantity.isnumeric() and int(units_quantity) > 0:
            children = self.adding_dialog.content_cls.panel.content

    async def _init_adding_dialog(self):
        ok_button = MDFlatButton(
            text='OK',
            theme_text_color='Custom',
            text_color=self.theme_cls.primary_color,
        )
        content_cls = Factory.AddingDialogCls()
        self.adding_dialog = MDDialog(
            title="Task's modal view",
            type='custom',
            content_cls=content_cls,
            buttons=[
                ok_button,
            ],
        )
        content_cls.root = self
        ok_button.bind(on_release=self.prepare_data_for_task_creation)

    async def _add_drop_down(self):
        items = await self._get_task_types_menu_items()
        self.task_types_menu = MDDropdownMenu(
            caller=self.drop_item,
            items=items,
            width_mult=4,
        )

    async def _get_task_types_menu_items(self):
        return [
            {
                "text": item.value.capitalize().replace('_', ' '),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=item.value: self._update_current_tasks_type(x),
            } for item in TaskTypes
        ]

    def _update_current_tasks_type(self, new_value):
        corrected_new_value = new_value.capitalize().replace('_', ' ')
        self.drop_item.text = corrected_new_value
        print(new_value)

    async def update_data_table_rows(self, tasks: List[Task] = None):
        if not tasks:
            self._tasks = []
            self._data_table.row_data = []
        else:
            self._tasks = tasks
            new_row_data = []
            self._data_table.row_data = new_row_data
            for task in tasks:
                new_row_data.append(
                    (
                        task.title,
                        datetime.datetime.strptime(task.deadline, "%Y-%m-%d"),
                        str(task.period),
                        task.status_title,
                        task.task_type_title,
                    )
                )

    def prepare_data_for_task_creation(self, *args):
        print('add')