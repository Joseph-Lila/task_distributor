""" Module src.domain.entities """


from dataclasses import Field, dataclass


@dataclass
class BaseEntity:
    """ Base entity class """

    item_id = Field(init=False)
