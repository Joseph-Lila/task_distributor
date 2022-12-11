""" Module src.domain.entities """
import datetime
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


@dataclass
class BaseTask(BaseEntity):
    """ Base Task entity """

    deadline: datetime.datetime
    title: str
    description: str
    status_id: int
    estimation: int
    register_id: int
