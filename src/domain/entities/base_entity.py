""" Module src.domain.entities """
from dataclasses import dataclass


@dataclass
class BaseEntity:
    """ Base entity class """

    item_id: int
