""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


@dataclass
class Complexity(BaseEntity):
    """ Complexity entity """

    title: str
    description: str
