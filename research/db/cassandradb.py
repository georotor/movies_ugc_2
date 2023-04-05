"""Модуль с тестами для Cassandra."""
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
    """Класс с тестами для Cassandra."""

    def __init__(self):
        """Подключение к БД и создание необходимых таблиц."""
        self.cluster = Cluster([settings.cassandra_host])
        self.session = self.cluster.connect()

        self.session.execute(SQL_CREATE_KEYSPACE)

        self.session.execute(SQL_CREATE_BOOKMARKS)
        self.session.execute(SQL_CREATE_LIKES)

    def close(self):
        """Очистка БД и закрытие соединения."""
        self.session.execute('DROP KEYSPACE research')
        self.cluster.shutdown()

    def bookmarks(self, bookmarks_data: list) -> list:
        """Тесты на чтение закладок."""
        insert = self.session.prepare('INSERT INTO research.bookmarks(user_id, film_ids) VALUES(?, ?)')
        for user_id, film_id in bookmarks_data:
            self.session.execute(insert, (user_id, (film_id,)))

        res = []

        for _ in range(settings.bookmarks_count):
            start = datetime.now()

            bookmark = random.choice(bookmarks_data)
            self.session.execute('SELECT * FROM research.bookmarks WHERE user_id=%s', (bookmark[0],)).one()

            end = datetime.now()
            res.append((end - start).microseconds)

        return res

    def likes(self, likes_data: list, film_ids: list) -> list:
        """Тесты на чтение средней оценки кинопроизведения."""
        insert = self.session.prepare('INSERT INTO research.likes(film_id, user_id, score) VALUES(?, ?, ?)')
        for row in likes_data:
            self.session.execute(insert, row)

        res = []

        for film_id in film_ids:
            start = datetime.now()

            self.session.execute('SELECT AVG (score) FROM research.likes WHERE film_id=%s', (film_id,)).one()

            end = datetime.now()
            res.append((end - start).microseconds)

        return res

    def likes_insert(self, likes_data: list) -> list:
        """Тесты на скорость записи лайков и последующем чтении средней оценки фильма."""
        res = []

        insert = self.session.prepare('INSERT INTO research.likes(film_id, user_id, score) VALUES(?, ?, ?)')
        for film_id, user_id, score in likes_data:
            start = datetime.now()

            self.session.execute(insert, (film_id, user_id, score))
            self.session.execute('SELECT AVG (score) FROM research.likes WHERE film_id=%s', (film_id,)).one()

            end = datetime.now()
            res.append((end - start).microseconds)

        return res
