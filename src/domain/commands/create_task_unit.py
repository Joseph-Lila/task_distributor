from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class CreateTaskUnit(Command):
    estimation: int
    status_title: str
    task_id: int
