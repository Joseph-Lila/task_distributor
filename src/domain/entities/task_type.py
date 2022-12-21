from dataclasses import dataclass

from src.domain.entities.base_entity import BaseEntity


@dataclass
class TaskType(BaseEntity):
    """  Represents Task Type entity """
    title: str
    description: str
