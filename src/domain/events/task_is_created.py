import datetime
from dataclasses import dataclass

from src.domain.events.event import Event


@dataclass
class TaskIsCreated(Event):
    id: int

