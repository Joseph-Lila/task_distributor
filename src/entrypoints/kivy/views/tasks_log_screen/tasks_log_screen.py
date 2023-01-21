import datetime
from typing import List, Optional

import asynckivy as ak
from dateutil.parser import parse
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.snackbar import Snackbar

from src.domain.entities.register import TASKS_DEFAULT_REGISTER
from src.domain.entities.status import Statuses
from src.domain.entities.task import NO_PERIOD_VALUE, Task
from src.domain.entities.task_type import TaskTypes
from src.entrypoints.kivy.controllers.abstract_controller import \
    do_with_loading_modal_view


class TasksLogScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_types_menu = None
        self.task_types_menu_for_cur_task = None
        self.date_dialog = None
        self.adding_dialog = None
        self._tasks = []
        self._cur_task: Optional[Task] = None
        self._init_view()

    def _init_view(self):
        ak.start(self._init_date_dialog())
        ak.start(self._add_drop_downs())
        self._update_current_tasks_type_request(TaskTypes.ALL.value)

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
                "on_release": lambda x=item.value: self._update_current_tasks_type_request(x),
            } for item in TaskTypes
        ]

    def update_tasks_cards_request(self):
        if self.drop_item.text == TaskTypes.ALL.value:
            ak.start(
                do_with_loading_modal_view(
                    self.controller.get_all_tasks
                )
            )
        else:
            ak.start(
                do_with_loading_modal_view(
                    self.controller.get_tasks_by_type,
                    self.drop_item.text
                )
            )

    def _update_current_tasks_type_request(self, new_value):
        self.drop_item.text = new_value
        if new_value == TaskTypes.ALL.value:
            ak.start(
                do_with_loading_modal_view(
                    self.controller.get_all_tasks
                )
            )
        else:
            ak.start(
                do_with_loading_modal_view(
                    self.controller.get_tasks_by_type,
                    new_value
                )
            )

    async def append_task_card(self, task: Task):
        self._tasks.append(task)
        new_widget = Factory.TaskItem()
        new_widget.item_id = task.item_id
        new_widget.title.text = task.title
        new_widget.deadline.text = str(task.deadline)
        new_widget.period.text = str(task.period)
        new_widget.status.text = task.status_title
        new_widget.type.text = task.task_type_title
        self.tasks.add_widget(new_widget)

    async def update_tasks_cards(self, tasks: List[Task] = None):
        self._tasks = []
        self.tasks.clear_widgets()
        if tasks:
            for task in tasks:
                await self.append_task_card(task)

    async def _get_task_forms_data(self):
        data = {
            'task_title': self.title_field.text_field.text,
            'deadline': self.date_field.text_field.text,
            'period': self.period_field.text_field.text,
            'task_description': self.description_field.text_field.text,
            'task_estimation': self.estimation_field.text_field.text,
            'task_type': self.task_type_drop_item.text,
        }
        return data

    def clear_task_form(self):
        self.title_field.text_field.text = ''
        self.date_field.text_field.text = ''
        self.period_field.text_field.text = ''
        self.description_field.text_field.text = ''
        self.estimation_field.text_field.text = ''
        self.task_type_drop_item.text = ''

    def fill_task_form(self, task: Task):
        self._cur_task = task
        self.title_field.text_field.text = task.title
        self.date_field.text_field.text = str(task.deadline)
        self.period_field.text_field.text = str(task.period)
        self.description_field.text_field.text = task.description
        self.estimation_field.text_field.text = str(task.estimation)
        self.status_field.text_field.text = task.status_title
        self.task_type_drop_item.text = task.task_type_title

    async def _check_common_adding_part(self, *args):
        data = await self._get_task_forms_data()
        if all(
                [
                    data['task_title'], data['deadline'], data['task_type'],
                    data['task_estimation']
                ]
        ):
            if data['task_type'] in [
                TaskTypes.COMMON_WITH_PERIOD.value, TaskTypes.NEGATIVE_WITH_PERIOD.value
            ] and not data['period']:
                return False
            return True
        return False

    async def _check_adding_form_is_filled(self, *args):
        common_part = await self._check_common_adding_part()
        if not common_part:
            Snackbar(text='Please, fill the fields...').open()
            return False
        return True

    async def delete_task_request(self, item_id):
        ak.start(
            do_with_loading_modal_view(
                self.controller.delete_task,
                item_id,
            )
        )

    async def edit_task_request(self, *args):
        data = await self._get_task_forms_data()
        filled = await self._check_adding_form_is_filled()
        if filled:
            item_id = self._cur_task.item_id
            title = data['task_title']
            deadline = parse(data['deadline'])
            period = int(data['period']) if data['period'] else NO_PERIOD_VALUE
            description = data['task_description']
            estimation = int(data['task_estimation']) if data['task_estimation'] else 0
            register_title = TASKS_DEFAULT_REGISTER
            task_type_title = data['task_type']
            complexity_title = self._cur_task.complexity_title

            ak.start(
                do_with_loading_modal_view(
                    self.controller.edit_task,
                    item_id, title, deadline, period, description, estimation, Statuses.IN_PROGRESS.value,
                    register_title, task_type_title, complexity_title,
                )
            )

    async def add_task_request(self, *args):
        data = await self._get_task_forms_data()
        filled = await self._check_adding_form_is_filled()
        if filled:
            title = data['task_title']
            deadline = parse(data['deadline']) if data['deadline'] else datetime.datetime.today()
            period = int(data['period']) if data['period'] else NO_PERIOD_VALUE
            description = data['task_description']
            estimation = int(data['task_estimation']) if data['task_estimation'] else 0
            register_title = TASKS_DEFAULT_REGISTER
            task_type_title = data['task_type']

            ak.start(
                do_with_loading_modal_view(
                    self.controller.create_task,
                    title, deadline, period, description, estimation, Statuses.IN_PROGRESS.value,
                    register_title, task_type_title,
                )
            )
