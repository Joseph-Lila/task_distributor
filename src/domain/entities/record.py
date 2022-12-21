""" Module src.domain.entities """
import datetime
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


@dataclass
class Record(BaseEntity):
    """ Record entity """

    what: str
    when: datetime.datetime
    how_much: float
    register_id: int
