import asyncio
import datetime
import math
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

from src.domain.entities.register import TASKS_DEFAULT_REGISTER
from src.domain.entities.status import Statuses
from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes
from src.entrypoints.kivy.controllers.abstract_controller import use_loop


class TasksLogScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_types_menu = None
        self.task_types_menu_for_cur_task = None
        self.date_dialog = None
        self.adding_dialog = None
        self._tasks = []
        self._init_view()

    def _init_view(self):
        ak.start(self._init_date_dialog())
        ak.start(self._add_drop_downs())
        self._update_current_tasks_type(TaskTypes.ALL.value)

    async def _init_date_dialog(self):
        self.date_dialog = MDDatePicker(
            min_date=datetime.date.today(),
        )
        self.date_dialog.bind(on_save=self.on_save_date_dialog)

    def on_save_date_dialog(self, instance, value, date_range):
        self.date_field.text = str(value)

    async def edit_task(self, item_id):
        for task in self._tasks:
            if task.item_id == item_id:
                await self.controller.go_to_edit_screen(task)
                return
        raise ValueError('Impossible to edit task...')

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

    def update_table(self):
        if self.drop_item.text == TaskTypes.ALL.value:
            ak.start(self.controller.get_all_tasks())
        else:
            ak.start(self.controller.get_tasks_by_type(self.drop_item.text))

    def _update_current_tasks_type(self, new_value):
        self.drop_item.text = new_value
        if new_value == TaskTypes.ALL.value:
            ak.start(self.controller.get_all_tasks())
        else:
            ak.start(self.controller.get_tasks_by_type(new_value))

    async def append_data_table_row(self, task: Task):
        self._tasks.append(task)
        new_widget = Factory.TaskItem()
        new_widget.item_id = task.item_id
        new_widget.title.text = task.title
        new_widget.deadline.text = str(task.deadline)
        new_widget.period.text = str(task.period)
        new_widget.status.text = task.status_title
        new_widget.type.text = task.task_type_title
        self.tasks.add_widget(new_widget)

    async def update_data_table_rows(self, tasks: List[Task] = None):
        self._tasks = []
        self.tasks.clear_widgets()
        if tasks:
            for task in tasks:
                await self.append_data_table_row(task)

    async def _check_complex_adding_part(self, *args):
        data = await self._get_task_forms_data()
        if data['task_type'] == TaskTypes.COMPLEX.value and data['units_common_title'] and data['min_per_unit']:
            return True
        elif data['task_type'] != TaskTypes.COMPLEX.value:
            return True
        return False

    async def _get_task_forms_data(self):
        units = None
        data = {
            'task_title': self.title_field.text_field.text,
            'deadline': self.date_field.text_field.text,
            'period': self.period_field.text_field.text,
            'task_description': self.description_field.text_field.text,
            'task_estimation': self.estimation_field.text_field.text,
            'task_type': self.task_type_drop_item.text,
            'units_common_title': self.common_title_field.text_field.text,
            'min_per_unit': self.measure_field.text_field.text,
            'units': units,
        }
        return data

    async def _check_common_adding_part(self, *args):
        data = await self._get_task_forms_data()
        if all(
                [
                    data['task_title'], data['deadline'], data['period'],
                    data['task_description'], data['task_estimation'], data['task_type'],
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
        data = await self._get_task_forms_data()
        filled = await self._check_adding_form_is_filled()
        if filled:
            title = data['task_title']
            deadline = parse(data['deadline'])
            period = int(data['period'])
            description = data['task_description']
            estimation = int(data['task_estimation'])
            register_title = TASKS_DEFAULT_REGISTER
            task_type_title = data['task_type']

            await self.controller.create_task(
                title, deadline, period, description, estimation,
                Statuses.IN_PROGRESS.value, register_title, task_type_title,
                data['units']
            )
