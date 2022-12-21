import asyncio

import aiosqlite
from src.config import get_sqlite_connection_str
import pathlib

CREATE_REGISTERS_TABLE = "CREATE TABLE IF NOT EXISTS registers(" \
                         "id INT PRIMARY KEY," \
                         "title TEXT," \
                         "description TEXT" \
                         ");"
CREATE_RECORDS_TABLE = "CREATE TABLE IF NOT EXISTS records(" \
                       "id INT PRIMARY KEY," \
                       "what TEXT," \
                       "when_ TEXT," \
                       "how_much REAL," \
                       "register_id INT," \
                       "FOREIGN KEY (register_id) REFERENCES registers(id)" \
                       "ON DELETE CASCADE ON UPDATE CASCADE" \
                       ");"
CREATE_TASK_TYPES_TABLE = "CREATE TABLE IF NOT EXISTS task_types(" \
                          "id INT PRIMARY KEY," \
                          "title TEXT," \
                          "description TEXT" \
                          ");"
CREATE_STATUSES_TABLE = "CREATE TABLE IF NOT EXISTS statuses(" \
                        "id INT PRIMARY KEY," \
                        "title TEXT," \
                        "description TEXT" \
                        ");"
CREATE_COMPLEXITIES_TABLE = "CREATE TABLE IF NOT EXISTS complexities(" \
                            "id INT PRIMARY KEY," \
                            "title TEXT," \
                            "description TEXT" \
                            ");"
CREATE_TASKS_TABLE = "CREATE TABLE IF NOT EXISTS tasks(" \
                     "id INT PRIMARY KEY," \
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
CREATE_UNITS_TABLE = "CREATE TABLE IF NOT EXISTS units(" \
                     "id INT PRIMARY KEY," \
                     "estimation INT," \
                     "status_id INT," \
                     "task_id INT," \
                     "FOREIGN KEY (status_id) REFERENCES statuses(id) ON DELETE CASCADE ON UPDATE CASCADE," \
                     "FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE ON UPDATE CASCADE" \
                     ");"

CREATE_CONSTRUCTIONS = [
    CREATE_REGISTERS_TABLE,
    CREATE_RECORDS_TABLE,
    CREATE_TASK_TYPES_TABLE,
    CREATE_STATUSES_TABLE,
    CREATE_COMPLEXITIES_TABLE,
    CREATE_TASKS_TABLE,
    CREATE_UNITS_TABLE,
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
    if not check_db_file_exists():
        with open(get_sqlite_connection_str(), 'w'):
            pass
    async with aiosqlite.connect(get_sqlite_connection_str()) as db:
        for command in CREATE_CONSTRUCTIONS:
            await db.execute(command)
        await db.commit()


if __name__ == "__main__":
    asyncio.run(create_tables())
