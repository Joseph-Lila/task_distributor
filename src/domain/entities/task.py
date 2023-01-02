import datetime
from dataclasses import dataclass
from typing import List, Optional, Union

from src.domain.entities.base_entity import BaseEntity
from src.domain.entities.unit import Unit


@dataclass
class Task(BaseEntity):
    """ Task entity. Some fields can be None. It depends on task type. """
    title: str
    deadline: Union[datetime.datetime, str]
    period: int
    place: Optional[int]
    description: str
    estimation: int
    status_title: str
    complexity_title: str
    register_title: str
    task_type_title: str
    units: Optional[List[Unit]]
