""" Module src.domain.entities """
from dataclasses import dataclass, field


@dataclass
class BaseEntity:
    """ Base entity class """

    item_id: int = field(init=False)
