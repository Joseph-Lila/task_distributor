from dataclasses import dataclass
from typing import Optional

from src.domain.commands.command import Command


@dataclass
class GetMainTask(Command):
    current_task_place: Optional[int]
