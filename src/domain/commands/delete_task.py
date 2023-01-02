from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class DeleteTask(Command):
    task_id: int
