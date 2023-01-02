""" Module src.domain.entities """
import enum
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


class Statuses(enum.Enum):
    DONE = 'DONE'
    FROZEN = 'FROZEN'
    IN_PROGRESS = 'IN PROGRESS'


@dataclass
class Status(BaseEntity):
    """ Status class entity """

    title: str
    description: str
