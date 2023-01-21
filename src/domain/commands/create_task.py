import datetime
from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class CreateTask(Command):
    title: str
    deadline: datetime.datetime
    period: int
    description: str
    estimation: int
    status_title: str
    register_title: str
    task_type_title: str
