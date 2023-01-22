from dataclasses import dataclass

from src.domain.entities.task import Task
from src.domain.events.event import Event


@dataclass
class GotMainTask(Event):
    task: Task
