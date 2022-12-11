""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.base_periodic_task import BasePeriodicTask
from src.domain.entities.negative_task import NegativeTask


@dataclass
class NegativePeriodicTask(NegativeTask, BasePeriodicTask):
    """ Negative Periodic Task entity """
