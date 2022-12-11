""" Module src.domain.entities """
from dataclasses import dataclass

from src.domain.entities.common_task import CommonTask


@dataclass
class SpecialTask(CommonTask):
    """ Special Task entity """
