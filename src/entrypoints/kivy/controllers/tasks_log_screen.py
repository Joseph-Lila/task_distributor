import datetime

from kivy.clock import mainthread

from src.domain.commands.create_task import CreateTask
from src.domain.commands.delete_task import DeleteTask
from src.domain.commands.edit_task import EditTask
from src.domain.commands.get_all_tasks import GetAllTasks
from src.domain.commands.get_tasks_by_type import GetTasksByType
from src.domain.entities.task import Task
from src.domain.entities.task_type import TaskTypes
from src.domain.events.task_is_created import TaskIsCreated
from src.domain.events.task_is_edited import TaskIsEdited
from src.entrypoints.kivy.controllers.abstract_controller import (
    AbstractController, use_loop)
from src.entrypoints.kivy.views.tasks_log_screen.tasks_log_screen import \
    TasksLogScreenView


class TasksLogScreenController(AbstractController):
    def __init__(self, bus):
        self.bus = bus
        self._view = TasksLogScreenView(controller=self)
        super().__init__()

    def get_view(self):
        return self._view

    @use_loop
    async def get_all_tasks(self):
        event = await self.bus.handle_command(GetAllTasks())
        if event:
            await self._view.update_tasks_cards(event.tasks)

    @use_loop
    async def get_tasks_by_type(self, status: str):
        event = await self.bus.handle_command(GetTasksByType(status))
        if event:
            await self._view.update_tasks_cards(event.tasks)

    @use_loop
    async def create_task(
            self, title: str, deadline: datetime.datetime, period: int,
            description: str, estimation: int, status_title: str,
            register_title: str, task_type_title: str
    ):
        # crate task
        event: TaskIsCreated = await self.bus.handle_command(
            CreateTask(
                title, deadline, period, description, estimation,
                status_title, register_title, task_type_title
            )
        )
        # update tasks cards
        if event:
            self._view.update_tasks_cards_request()
        self.go_to_table_screen()

    @use_loop
    async def delete_task(
            self,
            item_id,
    ):
        await self.bus.handle_command(
            DeleteTask(item_id)
        )
        # update tasks cards
        self._view.update_tasks_cards_request()
        self.go_to_table_screen()

    @use_loop
    async def edit_task(
            self, item_id: int, title: str, deadline: datetime.datetime, period: int,
            description: str, estimation: int, status_title: str, register_title: str,
            task_type_title: str, complexity_title: str,
    ):
        event: TaskIsEdited = await self.bus.handle_command(
            EditTask(
                item_id, title, deadline, period, description, estimation,
                status_title, register_title, task_type_title, complexity_title,
            )
        )
        # update tasks cards
        if event:
            self._view.update_tasks_cards_request()
        self.go_to_table_screen()

    @mainthread
    def _init_manipulations(self, *args):
        pass

    @staticmethod
    async def get_available_task_types():
        return [item.value for item in TaskTypes]

    def go_to_creation_screen(self, *args):
        self._view.operation_screen_manager.current = 'add'
        self._view.task_log_screen_manager.current = 'tasks fields screen'

    def go_to_table_screen(self, *args):
        self._view.task_log_screen_manager.current = 'table'
        self._view.clear_task_form()

    async def go_to_edit_screen(self, task: Task):
        self._view.fill_task_form(task)
        self._view.operation_screen_manager.current = 'edit'
        self._view.task_log_screen_manager.current = 'tasks fields screen'
