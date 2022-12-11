""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.base_task import BaseTask


@dataclass
class NegativeTask(BaseTask):
    """ Negative Task entity """
