import datetime

import pytest

from src.domain.entities.complexity import Complexities
from src.domain.entities.task import Task
from src.service_layer.handlers import time_to_minutes, get_working_minutes_before_the_deadline, get_urgency, \
    get_hottest_task_index, define_complexity


@pytest.mark.asyncio
async def test_time_to_minutes():
    date = datetime.datetime(year=2000, month=1, day=1, hour=2, minute=5, second=11)
    assert await time_to_minutes(date) == 2 * 60 + 5


@pytest.mark.asyncio
async def test_get_working_minutes_before_the_deadline():
    date = datetime.datetime(year=2023, month=1, day=12, hour=12, minute=52)
    now = datetime.datetime(year=2023, month=1, day=1, hour=16, minute=15)
    assert await get_working_minutes_before_the_deadline(date, now) == 15667


@pytest.mark.asyncio
async def test_get_urgency():
    date = datetime.datetime(year=2023, month=1, day=12, hour=12, minute=52)
    now = datetime.datetime(year=2023, month=1, day=1, hour=16, minute=15)
    estimation = 1000
    assert await get_urgency(date, estimation, now) == 14667


@pytest.mark.asyncio
async def test_get_hottest_task():
    task_1 = Task(
        item_id=1, title='1',
        deadline=datetime.datetime(year=2023, month=1, day=12, hour=12, minute=52),
        register_title='', task_type_title='', period=-1,
        estimation=1000, description='', status_title='',
        complexity_title='', place=None,
    )
    task_2 = Task(
        item_id=2, title='2',
        deadline=datetime.datetime(year=2023, month=1, day=12, hour=12, minute=52),
        register_title='', task_type_title='', period=-1,
        estimation=1001, description='', status_title='',
        complexity_title='', place=None,
    )
    task_3 = Task(
        item_id=2, title='2',
        deadline=datetime.datetime(year=2023, month=1, day=12, hour=12, minute=52),
        register_title='', task_type_title='', period=-1,
        estimation=999, description='', status_title='',
        complexity_title='', place=None,
    )
    assert await get_hottest_task_index([task_1, task_2, task_3]) == 1
    assert await get_hottest_task_index([task_1, task_3]) == 0
    assert await get_hottest_task_index([task_2, task_3]) == 0


@pytest.mark.asyncio
async def test_define_complexity():
    assert await define_complexity(-1) == Complexities.IMPOSSIBLE.value
    assert await define_complexity(0) == Complexities.CRITICAL.value
    assert await define_complexity(1) == Complexities.HARD.value
    assert await define_complexity(1439) == Complexities.HARD.value
    assert await define_complexity(1440) == Complexities.MEDIUM.value
    assert await define_complexity(1441) == Complexities.MEDIUM.value
    assert await define_complexity(1440 * 7 - 1) == Complexities.MEDIUM.value
    assert await define_complexity(1440 * 7) == Complexities.EASY.value
    assert await define_complexity(1440 * 7 + 1) == Complexities.EASY.value
    assert await define_complexity(1440 * 7 + 2) == Complexities.EASY.value
