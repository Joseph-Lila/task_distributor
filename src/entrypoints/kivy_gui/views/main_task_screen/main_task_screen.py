from typing import Optional, List

import asynckivy as ak
from kivy.properties import ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.taptargetview import MDTapTargetView

from src.domain.entities.task import Task


class MainTaskScreenView(MDBottomNavigationItem):
    controller = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tap_target_view = None
        self.current_task: Optional[Task] = None
        self.current_negative_task: Optional[Task] = None
        self.negative_tasks: List[Task] = []
        self._init_view()

    def on_enter(self, *args):
        ak.start(self.controller.setup_tasks())
        ak.start(self.controller.get_negative_tasks())
        ak.start(self.controller.get_main_task())

    def _init_view(self):
        self._tap_target_view = MDTapTargetView(
            widget=self.more_button,
            title_text='No text',
            title_text_size="36sp",
            title_text_color=(204/255, 191/255, 0, 1),
            description_text='No text',
            description_text_color=(0, 141/255, 142/255, 1),
            widget_position='bottom',
            outer_circle_color=(1, 1, 1)
        )

    def tap_target_start(self):
        if self._tap_target_view.state == "close":
            self._tap_target_view.start()
        else:
            self._tap_target_view.stop()

    async def update_negative_task(self, cur_negative_task: Optional[Task] = None):
        if not cur_negative_task:
            self.cur_negative_info_btn.disabled = True
            self.next_negative_btn.disabled = True
            self.cur_negative_title.text = 'Empty ...'
        else:
            self.current_negative_task = cur_negative_task
            self.cur_negative_info_btn.disabled = False
            self.next_negative_btn.disabled = False
            self.cur_negative_title.text = cur_negative_task.title

    async def update_negative_tasks_quantity(self, quantity: Optional[int] = None):
        if not quantity:
            self.negative_tasks_quantity.text = '?'
        else:
            self.negative_tasks_quantity.text = str(quantity)

    async def get_next_negative_task(self):
        cur_task_index = self.negative_tasks.index(self.current_negative_task)
        if cur_task_index == len(self.negative_tasks) - 1:
            await self.update_negative_task(self.negative_tasks[0])
        else:
            await self.update_negative_task(self.negative_tasks[cur_task_index + 1])

    async def update_current_task(self, cur_task: Optional[Task] = None):
        if not cur_task:
            self.more_button.disabled = True
            self.cur_task_title.text = 'Empty...'
            self.froze_btn.disabled = True
            self.skip_btn.disabled = True
            self.accept_btn.disabled = True
        else:
            self.current_task = cur_task
            self._tap_target_view.title_text = cur_task.complexity_title
            self._tap_target_view.description_text = cur_task.description if cur_task.description else 'Empty...'
            self.cur_task_title.text = cur_task.title
            self.more_button.disabled = False
            self.froze_btn.disabled = False
            self.skip_btn.disabled = False
            self.accept_btn.disabled = False
