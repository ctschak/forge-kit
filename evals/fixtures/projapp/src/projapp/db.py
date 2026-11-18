import os
import sqlite3

MIGRATIONS = os.path.join(os.path.dirname(__file__), "..", "..", "db", "migrations")


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    for name in sorted(os.listdir(MIGRATIONS)):
        with open(os.path.join(MIGRATIONS, name)) as fh:
            conn.executescript(fh.read())
    return conn
