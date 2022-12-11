""" Module src.adapters """
from sqlalchemy import (Column, DateTime, Integer, MetaData,
                        String, Table)
from sqlalchemy.orm import mapper

from src.domain.entities.common_task import CommonTask

metadata = MetaData()

common_tasks = Table(
    "common_tasks",
    metadata,
    Column("item_id", Integer, primary_key=True, autoincrement=True),
    Column("deadline", DateTime, nullable=False),
    Column("title", String, nullable=False),
    Column("description", String, nullable=True),
    Column("status_id", Integer, nullable=False),
    Column("estimation", Integer, nullable=False),
    Column("register_id", Integer, nullable=False),
    Column("place", Integer, nullable=True),
    Column("complexity_id", Integer, nullable=True)
)


def start_mappers():
    """ Method to map entities with db tables """
    # common_tasks_mapper = mapper(CommonTask, common_tasks)
    mapper(CommonTask, common_tasks)
