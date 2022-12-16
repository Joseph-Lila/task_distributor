""" Module tests """
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy_aio import ASYNCIO_STRATEGY
from src.adapters.orm import metadata, start_mappers


@pytest.fixture
async def in_memory_db():
    """ Method to get in memory database """
    engine = create_engine("sqlite:///:memory:", strategy=ASYNCIO_STRATEGY)
    await metadata.create_all(engine)
    return engine


@pytest.fixture
async def session(in_memory_db):
    """ Method returns session maker as generator """
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
