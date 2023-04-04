import random
from datetime import datetime

from cassandra.cluster import Cluster

from config import settings


SQL_CREATE_KEYSPACE = """
    CREATE KEYSPACE IF NOT EXISTS research 
    WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' }
"""

SQL_CREATE_BOOKMARKS = """
    CREATE TABLE IF NOT EXISTS research.bookmarks (
        user_id uuid PRIMARY KEY,
        film_ids set<uuid>
    )
"""

SQL_CREATE_LIKES = """
    CREATE TABLE IF NOT EXISTS research.likes (
        film_id uuid,
        user_id uuid,
        score smallint,
        PRIMARY KEY (film_id, user_id)
    )
"""


class TestCassandra:
    def __init__(self):
        self.cluster = Cluster([settings.cassandra_host])
        self.session = self.cluster.connect()

        self.session.execute(SQL_CREATE_KEYSPACE)
        self.session.set_keyspace('research')

        self.session.execute(SQL_CREATE_BOOKMARKS)
        self.session.execute(SQL_CREATE_LIKES)

    def close(self):
        self.session.execute('DROP KEYSPACE research')
        self.cluster.shutdown()

    def bookmarks(self, data: list) -> list:
        insert = self.session.prepare('INSERT INTO bookmarks(user_id, film_ids) VALUES(?, ?)')
        for user_id, film_id in data:
            self.session.execute(insert, (user_id, (film_id,)))

        res = []

        for _ in range(settings.bookmarks_count):
            start = datetime.now()

            user_id, film_id = random.choice(data)
            self.session.execute("SELECT * FROM bookmarks WHERE user_id={}".format(user_id)).one()

            end = datetime.now()
            res.append((end - start).microseconds)

        return res

    def likes(self, data: list, film_ids: list) -> list:
        insert = self.session.prepare('INSERT INTO likes(film_id, user_id, score) VALUES(?, ?, ?)')
        for row in data:
            self.session.execute(insert, row)

        res = []

        for film_id in film_ids:
            start = datetime.now()

            self.session.execute("SELECT AVG (score) FROM likes WHERE film_id={}".format(film_id)).one()

            end = datetime.now()
            res.append((end - start).microseconds)

        return res

    def likes_insert(self, data: list) -> list:
        res = []

        insert = self.session.prepare('INSERT INTO likes(film_id, user_id, score) VALUES(?, ?, ?)')
        for film_id, user_id, score in data:
            start = datetime.now()

            self.session.execute(insert, (film_id, user_id, score))
            self.session.execute("SELECT AVG (score) FROM likes WHERE film_id={}".format(film_id)).one()

            end = datetime.now()
            res.append((end - start).microseconds)

        return res
