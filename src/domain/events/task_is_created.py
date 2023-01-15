import datetime
from dataclasses import dataclass

from src.domain.events.event import Event


@dataclass
class TaskIsCreated(Event):
    id: int
    title: str
    deadline: datetime.datetime
    period: int
    description: str
    estimation: int
    status_title: str
    register_title: str
    task_type_title: str
