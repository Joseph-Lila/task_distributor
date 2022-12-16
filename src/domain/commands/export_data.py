from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class ExportData(Command):
    path: str
