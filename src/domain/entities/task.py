import datetime
from dataclasses import dataclass
from typing import List, Optional, Union

from src.domain.entities.base_entity import BaseEntity

NO_PERIOD_VALUE = -1
DAY_START = datetime.time(hour=4, minute=0)
DAY_END = datetime.time(hour=22, minute=0)


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
