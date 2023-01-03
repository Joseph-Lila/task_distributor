from datetime import datetime
from typing import List
import asynckivy as ak
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.datatables import MDDataTable

from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes


class TasksLogScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_table = None
        self._tasks: List[Task] = []
        self._init_view()

    def _init_view(self):
        ak.start(self._add_data_table())
        ak.start(self._add_drop_down())

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

    async def _add_drop_down(self):
        pass

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
                        datetime.strptime(task.deadline, "%Y-%m-%d"),
                        str(task.period),
                        task.status_title,
                        task.task_type_title,
                    )
                )
