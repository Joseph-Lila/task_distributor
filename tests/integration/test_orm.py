"""Module tests.unit """
import datetime

from sqlalchemy import insert

from src.domain.entities.common_task import CommonTask


def test_common_task_mapper_can_load_tasks(session):
    # prepare data
    values = [
        {
            'deadline': datetime.datetime.now(), 'title': 'title1', 'description': 'description1',
            'status_id': 1, 'estimation': 1, 'register_id': 1, 'place': 1, 'complexity_id': 1,
        },
        {
            'deadline': datetime.datetime.now(), 'title': 'title2', 'description': 'description2',
            'status_id': 2, 'estimation': 2, 'register_id': 2, 'place': 2, 'complexity_id': 2,
        },
    ]

    # add data to in memory db
    for value in values:
        statement = insert(CommonTask).values(
            **value
        )
        session.execute(statement)

    # since expected data has no item_ids, add them
    expected = [CommonTask(**values_item) for values_item in values]
    for i in range(len(expected)):
        expected[i].item_id = i + 1

    assert session.query(CommonTask).all() == expected
