import datetime
from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class MarkTaskAsInProgress(Command):
    task_id: int
    estimation: int
    deadline: datetime.datetime
