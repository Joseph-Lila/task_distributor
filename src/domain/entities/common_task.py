""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.base_task import BaseTask


@dataclass
class CommonTask(BaseTask):
    """ Common Task entity """

    place: int
    complexity_id: int
