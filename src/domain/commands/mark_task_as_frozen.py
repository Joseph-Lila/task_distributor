from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class MarkTaskAsFrozen(Command):
    task_id: int
