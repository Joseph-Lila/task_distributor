""" Module src.adapters.repositories.sql_alchemy_repositories """
from src.adapters.repositories.abstract_repository import AbstractRepository
from src.domain.entities.base_entity import BaseEntity
from src.domain.entities.common_task import CommonTask


class CommonTaskRepository(AbstractRepository):
    """ Common Task Repository implementation """

    def __init__(self, session):
        self.session = session

    def get(self, item_id: int):
        """ Method to get object from database """
        return self.session.query(CommonTask).filter_by(item_id=item_id).one()

    def add(self, new_element: BaseEntity):
        """ Method to add new element to the session """
        self.session.add(new_element)
