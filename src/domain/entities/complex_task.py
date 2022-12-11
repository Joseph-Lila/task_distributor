""" Module src.domain.entities """
from typing import List

from src.domain.entities.common_task import CommonTask
from src.domain.entities.unit import Unit


class ComplexTask(CommonTask):
    """ Complex Task entity """

    def __init__(self, units: List[Unit]):
        super().__init__()
        self.units = units

    def calculate_estimation(self):
        """ Method to calculate real estimation. Returns remainder. """
        pass
