import datetime
from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class EditTask(Command):
    task_id: int
    title: str
    deadline: datetime.datetime
    period: int
    description: str
    estimation: int
    status_title: str
    register_title: str
    task_type_title: str
    complexity_title: str
