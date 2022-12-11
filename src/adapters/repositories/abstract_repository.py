""" Module src.adapters.repositories """
import abc

from src.domain.entities.base_entity import BaseEntity


class AbstractRepository(abc.ABC):
    """ Abstract Repository class """

    @abc.abstractmethod
    def add(self, new_element: BaseEntity):
        """ Method to add new element to session """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, item_id: int):
        """ Method to get element using `item_id` field """
        raise NotImplementedError
