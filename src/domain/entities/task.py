import datetime
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


@dataclass
class Task(BaseEntity):
    """ Task entity. Some fields can be None. It depends on task type. """
    title: str
    deadline: datetime.datetime
    period: int
    place: int
    description: str
    estimation: int
    status_id: int
    complexity_id: int
    register_id: int
    task_type_id: int
