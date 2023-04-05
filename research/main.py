"""Тестирование производительности БД Mongo и Cassandra."""
import logging
from datetime import timedelta
from math import log
from random import choice, randint
from uuid import uuid4

from config import settings
from db.cassandradb import TestCassandra
from db.mongodb import TestMongo


logging.basicConfig(level=logging.INFO)


def res_format(db, res, size) -> str:
    """Форматирование результатов тестирования."""
    return '\t {0}: {1}, avg={2}, min={3}, max={4}'.format(
        db,
        timedelta(microseconds=sum(res)),
        timedelta(microseconds=sum(res) / size),
        timedelta(microseconds=min(res)),
        timedelta(microseconds=max(res)),
    )


def test_bookmarks(cassandra: TestCassandra, mongo: TestMongo):
    """Тесты на чтение закладок."""
    logging.info('Test reading {0} bookmarks:'.format(
        settings.bookmarks_count,
    ))

    bookmarks = []
    for _ in range(settings.bookmarks_count):
        bookmarks.append((uuid4(), uuid4()))

    res = cassandra.bookmarks(bookmarks)
    logging.info(res_format('cassandra', res, len(bookmarks)))
    res = mongo.bookmarks(bookmarks)
    logging.info(res_format('mongo', res, len(bookmarks)))


def test_likes(cassandra: TestCassandra, mongo: TestMongo):
    """Тесты на чтение средней оценки кинопроизведения."""
    likes = []
    films_count = int(log(settings.likes_count, settings.films_count_factor))
    film_ids = [uuid4() for _ in range(films_count)]

    logging.info('Test average rating of {0} films in {1} likes:'.format(
        len(film_ids),
        settings.likes_count,
    ))

    for _ in range(settings.likes_count):
        likes.append((
            choice(film_ids),
            uuid4(),
            randint(0, 10),
        ))

    res = cassandra.likes(likes, film_ids)
    logging.info(res_format('cassandra', res, len(film_ids)))
    res = mongo.likes(likes, film_ids)
    logging.info(res_format('mongo', res, len(film_ids)))


def test_likes_insert(cassandra: TestCassandra, mongo: TestMongo):
    """Тесты на скорость записи лайков и последующем чтении средней оценки фильма."""
    likes = []
    films_count = int(log(settings.likes_count, settings.films_count_factor))
    film_ids = [uuid4() for _ in range(films_count)]

    logging.info('Test insert data and read average rating of {0} films in {1} likes:'.format(
        len(film_ids),
        settings.likes_count,
    ))

    for _ in range(settings.likes_count):
        likes.append((
            choice(film_ids),
            uuid4(),
            randint(0, 10),
        ))

    res = cassandra.likes_insert(likes)
    logging.info(res_format('cassandra', res, len(likes)))
    res = mongo.likes_insert(likes)
    logging.info(res_format('mongo', res, len(likes)))


def start():
    """Запускаем тесты."""
    cassandra = TestCassandra()
    mongo = TestMongo()

    test_bookmarks(cassandra, mongo)
    test_likes(cassandra, mongo)
    test_likes_insert(cassandra, mongo)

    cassandra.close()
    mongo.close()


if __name__ == '__main__':
    start()
