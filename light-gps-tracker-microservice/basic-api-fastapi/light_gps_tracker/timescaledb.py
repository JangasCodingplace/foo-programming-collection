import psycopg2.pool
from functools import partial
from config import TIMESCALE_DB


class _TimeScaleHandler:
    def __init__(self, pool: psycopg2.pool):
        self.pool = pool

    def __enter__(self):
        self.conn = self.pool.getconn()
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, *args, **kwargs):
        self.cursor.close()
        self.pool.putconn(self.conn)
        return

    def execute(self, query: str, *args):
        self.cursor.execute(query, *args)

    def fetchone(self, query: str, *args):
        self.execute(query, *args)
        return self.cursor.fetchone()

    def fetchall(self, query: str, *args):
        self.execute(query, *args)
        return self.cursor.fetchall()


_timescaledb_connection_pool = psycopg2.pool.SimpleConnectionPool(**TIMESCALE_DB)
TimeScaleHandler = partial(_TimeScaleHandler, pool=_timescaledb_connection_pool)
