import datetime

from src.domain.commands.allocate_tasks import AllocateTasks
from src.domain.commands.get_main_task import GetMainTask
from src.domain.commands.get_tasks_by_type import GetTasksByType
from src.domain.commands.mark_task_as_done import MarkTaskAsDone
from src.domain.commands.mark_task_as_frozen import MarkTaskAsFrozen
from src.domain.commands.setup_tasks import SetupTasks
from src.domain.entities.task_type import TaskTypes
from src.domain.events.got_all_tasks import GotAllTasks
from src.domain.events.got_main_task import GotMainTask
from src.entrypoints.kivy_gui.controllers.abstract_controller import (
    AbstractController, use_loop)
from src.entrypoints.kivy_gui.views.main_task_screen.main_task_screen import \
    MainTaskScreenView


class MainTaskScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = MainTaskScreenView(controller=self)

    def get_view(self):
        return self._view

    @use_loop
    async def get_main_task(self, current_task_place=None):
        await self.bus.handle_command(
            AllocateTasks()
        )
        event: GotMainTask = await self.bus.handle_command(GetMainTask(current_task_place))
        await self._view.update_current_task(event.task)

    @use_loop
    async def get_negative_tasks(self):
        tasks = []
        for task_type in [TaskTypes.NEGATIVE.value, TaskTypes.NEGATIVE_WITH_PERIOD.value]:
            event: GotAllTasks = await self.bus.handle_command(GetTasksByType(task_type))
            if event:
                tasks.extend(event.tasks)
        tasks = [
            task for task in tasks
            if (task.deadline - datetime.timedelta(days=task.estimation / 1440)).date() <= datetime.datetime.now().date()
        ]
        self._view.negative_tasks = tasks
        if tasks:
            await self._view.update_negative_task(tasks[0])
            await self._view.update_negative_tasks_quantity(len(tasks))
        else:
            await self._view.update_negative_task()
            await self._view.update_negative_tasks_quantity()

    @use_loop
    async def mark_task_as_done(self, task_id: int):
        await self.bus.handle_command(
            MarkTaskAsDone(task_id)
        )
        await self.get_main_task()

    @use_loop
    async def mark_task_as_frozen(self, task_id: int):
        await self.bus.handle_command(
            MarkTaskAsFrozen(task_id)
        )
        await self.get_main_task()

    @use_loop
    async def setup_tasks(self):
        await self.bus.handle_command(
            SetupTasks()
        )
