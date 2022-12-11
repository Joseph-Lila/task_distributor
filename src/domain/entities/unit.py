""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


@dataclass
class Unit(BaseEntity):
    """ Unit entity """

    estimation: int
    status_id: int
