""" Module src.domain.entities """
from dataclasses import dataclass


@dataclass
class BasePeriodicTask:
    """ Base Periodic Task entity """

    period: int
