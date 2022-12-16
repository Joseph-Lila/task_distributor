import pytest
from src.service_layer.unit_of_work.aiosqlite_unit_of_work import AiosqliteUnitOfWork


@pytest.mark.asyncio
async def test_transaction(in_memory_sqlite_db):
    uow = AiosqliteUnitOfWork(connection_string=in_memory_sqlite_db)
    async with uow:
        assert in_memory_sqlite_db == ':memory:'
