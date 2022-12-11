""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.base_periodic_task import BasePeriodicTask
from src.domain.entities.common_task import CommonTask


@dataclass
class PeriodicTask(CommonTask, BasePeriodicTask):
    """ Periodic Task entity """
