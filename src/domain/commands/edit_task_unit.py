from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class EditTaskUnit(Command):
    task_unit_id: int
    estimation: int
    status_title: str
