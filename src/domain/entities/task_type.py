import enum
from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


class TaskTypes(enum.Enum):
    ALL = 'ALL'
    COMMON = 'COMMON'
    COMMON_WITH_PERIOD = 'COMMON_WITH_PERIOD'
    NEGATIVE = 'NEGATIVE'
    NEGATIVE_WITH_PERIOD = 'NEGATIVE_WITH_PERIOD'
    SPECIAL = 'SPECIAL'


@dataclass
class TaskType(BaseEntity):
    """  Represents Task Type entity """
    title: str
    description: str
