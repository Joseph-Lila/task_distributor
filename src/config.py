""" Module sre """
import pathlib

THIS_DIR = pathlib.Path(__file__).parent.resolve().absolute()
ROOT_DIR = THIS_DIR.parent


def get_sqlite_connection_str():
    """
    Returns path to sqlite database.
    :return: pathlib.Path
    """
    db_path = ROOT_DIR / 'assets' / 'databases' / 'sqlite.db'
    if db_path.exists():
        return str(db_path)
    else:
        return ':memory:'
