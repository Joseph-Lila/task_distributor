from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetAnotherTask(Command):
    current_task_place: int
