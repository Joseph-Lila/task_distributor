from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class MarkTaskAsDone(Command):
    task_id: int
