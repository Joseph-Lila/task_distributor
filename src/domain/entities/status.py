""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


@dataclass
class Status(BaseEntity):
    """ Status class entity """

    title: str
    description: str
