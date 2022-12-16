import pytest


@pytest.fixture
def in_memory_sqlite_db():
    """
    Method to get in memory sqlite db
    :return: str
    """
    return ':memory:'
