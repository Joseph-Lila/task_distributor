from dataclasses import dataclass
from typing import List

from src.domain.entities.task import Task
from src.domain.events.event import Event


@dataclass
class GotAllTasks(Event):
    tasks: List[Task]
