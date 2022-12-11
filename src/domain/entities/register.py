""" Module src.domain.entities """
from dataclasses import dataclass
from typing import List

from src.domain.entities.base_entity import BaseEntity
from src.domain.entities.record import Record


@dataclass
class Register(BaseEntity):
    """ Register entity """

    title: str
    description: str
    records: List[Record]
    with_task: bool
