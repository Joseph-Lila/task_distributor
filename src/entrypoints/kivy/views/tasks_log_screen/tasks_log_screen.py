import asyncio
import datetime
from functools import partial
from typing import List

import asynckivy as ak
from dateutil.parser import parse
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
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField

from src.domain.entities.register import TASKS_REGISTER
from src.domain.entities.status import Statuses
from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes
from src.entrypoints.kivy.controllers.abstract_controller import use_loop


class TasksLogScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_table = None
        self.task_types_menu = None
        self.task_types_menu_for_cur_task = None
        self.date_dialog = None
        self.adding_dialog = None
        self._tasks: List[Task] = []
        self._init_view()

    def _init_view(self):
        ak.start(self._init_date_dialog())
        ak.start(self._add_data_table())
        ak.start(self._add_drop_downs())
        self._update_current_tasks_type(TaskTypes.ALL.value)

    async def _add_data_table(self):
        self._data_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("Title", dp(60)),
                ("Deadline", dp(45)),
                ("Period", dp(30)),
                ("Status", dp(45)),
                ("Type", dp(45)),
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
        self.date_field.text = str(value)

    async def _add_drop_downs(self):
        items = await self._get_task_types_menu_items()
        self.task_types_menu = MDDropdownMenu(
            caller=self.drop_item,
            items=items,
            width_mult=4,
        )

        items_for_current_task = await self._get_task_types_menu_items_for_cur_task()
        self.task_types_menu_for_cur_task = MDDropdownMenu(
            caller=self.task_type_drop_item,
            items=items_for_current_task,
            width_mult=4,
        )

    def _update_task_type_for_cur_task(self, new_value):
        self.task_type_drop_item.text = new_value

    async def _get_task_types_menu_items_for_cur_task(self):
        ans = [
            {
                "text": item.value,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=item.value: self._update_task_type_for_cur_task(x),
            } for item in TaskTypes
        ]
        ans.pop(0)
        return ans

    async def _get_task_types_menu_items(self):
        return [
            {
                "text": item.value,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=item.value: self._update_current_tasks_type(x),
            } for item in TaskTypes
        ]

    def _update_current_tasks_type(self, new_value):
        self.drop_item.text = new_value
        if new_value == TaskTypes.ALL.value:
            ak.start(self.controller.get_all_tasks())
        else:
            ak.start(self.controller.get_tasks_by_type(new_value))

    async def append_data_table_row(self, task: Task):
        self._tasks.append(task)
        self._data_table.row_data.append(
            (
                task.title,
                task.deadline,
                str(task.period),
                task.status_title,
                task.task_type_title,
            )
        )

    async def update_data_table_rows(self, tasks: List[Task] = None):
        self._tasks = []
        self._data_table.row_data = []
        if tasks:
            for task in tasks:
                await self.append_data_table_row(task)

    async def _check_complex_adding_part(self, *args):
        task_type_drop_item = self.task_type_drop_item.text
        common_title_field = self.common_title_field.text_field.text
        measure_field = self.measure_field.text_field.text
        if task_type_drop_item == TaskTypes.COMPLEX.value and common_title_field and measure_field:
            return True
        elif task_type_drop_item != TaskTypes.COMPLEX.value:
            return True
        return False

    async def _check_common_adding_part(self, *args):
        title_field = self.title_field.text_field.text
        date_field = self.date_field.text_field.text
        period_field = self.period_field.text_field.text
        description_field = self.description_field.text_field.text
        estimation_field = self.estimation_field.text_field.text
        task_type_drop_item = self.task_type_drop_item.text

        if all(
                [
                    title_field, date_field, period_field, description_field,
                    estimation_field, task_type_drop_item,
                ]
        ):
            return True
        return False

    async def _check_adding_form_is_filled(self, *args):
        complex_part = await self._check_complex_adding_part()
        common_part = await self._check_common_adding_part()
        if not (complex_part and common_part):
            Snackbar(text='Please, fill the fields...').open()
            return False
        return True

    async def prepare_data_for_adding(self, *args):
        filled = await self._check_adding_form_is_filled()
        if filled:
            title = self.title_field.text_field.text
            deadline = parse(self.date_field.text_field.text)
            period = int(self.period_field.text_field.text)
            description = self.description_field.text_field.text
            estimation = int(self.estimation_field.text_field.text)
            register_title = TASKS_REGISTER
            task_type_title = self.task_type_drop_item.text

            await self.controller.create_task(
                title, deadline, period, description, estimation,
                Statuses.IN_PROGRESS.value, register_title, task_type_title,
            )
