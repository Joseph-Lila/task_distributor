from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetTasksByType(Command):
    status_title: str
