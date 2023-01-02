""" Module src.domain.entities """
import enum
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


class Complexities(enum.Enum):
    UNDEFINED = 'UNDEFINED'
    EAZY = 'EAZY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'
    CRITICAL = 'CRITICAL'
    IMPOSSIBLE = 'IMPOSSIBLE'


@dataclass
class Complexity(BaseEntity):
    """ Complexity entity """

    title: str
    description: str
