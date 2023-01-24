import asyncio
import pathlib

import aiosqlite

from src.config import get_sqlite_connection_str

CREATE_REGISTERS_TABLE = "CREATE TABLE IF NOT EXISTS registers(" \
                         "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                         "title TEXT," \
                         "description TEXT" \
                         ");"
CREATE_RECORDS_TABLE = "CREATE TABLE IF NOT EXISTS records(" \
                       "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                       "what TEXT," \
                       "when_ TEXT," \
                       "how_much REAL," \
                       "register_id INT," \
                       "FOREIGN KEY (register_id) REFERENCES registers(id)" \
                       "ON DELETE CASCADE ON UPDATE CASCADE" \
                       ");"
CREATE_TASK_TYPES_TABLE = "CREATE TABLE IF NOT EXISTS task_types(" \
                          "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                          "title TEXT," \
                          "description TEXT" \
                          ");"
CREATE_STATUSES_TABLE = "CREATE TABLE IF NOT EXISTS statuses(" \
                        "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                        "title TEXT," \
                        "description TEXT" \
                        ");"
CREATE_COMPLEXITIES_TABLE = "CREATE TABLE IF NOT EXISTS complexities(" \
                            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                            "title TEXT," \
                            "description TEXT" \
                            ");"
CREATE_TASKS_TABLE = "CREATE TABLE IF NOT EXISTS tasks(" \
                     "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                     "title TEXT," \
                     "deadline TEXT," \
                     "period INT," \
                     "place INT," \
                     "description TEXT," \
                     "estimation INT," \
                     "status_id INT," \
                     "complexity_id INT," \
                     "register_id INT," \
                     "task_type_id INT," \
                     "FOREIGN KEY (status_id) REFERENCES statuses(id) ON DELETE CASCADE ON UPDATE CASCADE," \
                     "FOREIGN KEY (complexity_id) REFERENCES complexities(id) ON DELETE CASCADE ON UPDATE CASCADE," \
                     "FOREIGN KEY (register_id) REFERENCES registers(id) ON DELETE CASCADE ON UPDATE CASCADE," \
                     "FOREIGN KEY (task_type_id) REFERENCES task_types(id) ON DELETE CASCADE ON UPDATE CASCADE" \
                     ");"
ADD_TASKS_REGISTER_RECORD = "INSERT INTO registers (title, description) VALUES ('Tasks', 'Main register');"
ADD_STATUSES_RECORDS = [
    "INSERT INTO statuses (title, description) VALUES ('DONE', 'Task is completely done.'); ",
    "INSERT INTO statuses (title, description) VALUES ('FROZEN', 'Task is not completed and now is not activated.'); ",
    "INSERT INTO statuses (title, description) VALUES ('IN PROGRESS', 'Task is doing now.'); ",
]
ADD_TASK_TYPES_RECORDS = [
    "INSERT INTO task_types (title, description) VALUES ('COMMON', 'Such tasks may be completed once.'); ",
    "INSERT INTO task_types (title, description) VALUES ('COMMON_WITH_PERIOD', 'After task is completed it borns again.'); ",
    "INSERT INTO task_types (title, description) VALUES ('NEGATIVE', 'I do not need to do it till the deadline.'); ",
    "INSERT INTO task_types (title, description) VALUES ('NEGATIVE_WITH_PERIOD', 'I do not need to do it till the deadline again and again.'); ",
    "INSERT INTO task_types (title, description) VALUES ('SPECIAL', 'Must be done firstly.'); ",
]
ADD_COMPLEXITIES_RECORDS = [
    "INSERT INTO complexities (title, description) VALUES ('UNDEFINED', 'I need to analyze the situation.'); ",
    "INSERT INTO complexities (title, description) VALUES ('EASY', 'I have 100 hours more than I need before the deadline.'); ",
    "INSERT INTO complexities (title, description) VALUES ('MEDIUM', 'I have 60 hours more than I need before the deadline.'); ",
    "INSERT INTO complexities (title, description) VALUES ('HARD', 'I have 30 hours more than I need before the deadline.'); ",
    "INSERT INTO complexities (title, description) VALUES ('CRITICAL', 'I have estimation time sharply to complete this task.'); ",
    "INSERT INTO complexities (title, description) VALUES ('IMPOSSIBLE', 'There is 20% of estimated time before the deadline.'); ",
]

CREATE_CONSTRUCTIONS = [
    CREATE_REGISTERS_TABLE,
    CREATE_RECORDS_TABLE,
    CREATE_TASK_TYPES_TABLE,
    CREATE_STATUSES_TABLE,
    CREATE_COMPLEXITIES_TABLE,
    CREATE_TASKS_TABLE,
    ADD_TASKS_REGISTER_RECORD,
    *ADD_STATUSES_RECORDS,
    *ADD_TASK_TYPES_RECORDS,
    *ADD_COMPLEXITIES_RECORDS,
]


def check_db_file_exists():
    """
    Method to check if db_file exists.
    :return: Bool/None
    """
    if pathlib.Path(get_sqlite_connection_str()).exists():
        return True


async def create_tables():
    """
    Method to prepare db file and build tables
    :return: None
    """
    print('*' * 50)
    print('create tables!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if not check_db_file_exists():
        print('not exists(((')
        with open(get_sqlite_connection_str(), 'w'):
            pass
            print(get_sqlite_connection_str())
        async with aiosqlite.connect(get_sqlite_connection_str()) as db:
            for command in CREATE_CONSTRUCTIONS:
                await db.execute(command)
            await db.commit()


if __name__ == "__main__":
    asyncio.run(create_tables())
