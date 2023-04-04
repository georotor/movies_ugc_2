from datetime import timedelta
from uuid import uuid4
from math import log
from random import choice, randint

from config import settings
from db.cassandradb import TestCassandra
from db.mongodb import TestMongo


def res_format(db, res, size):
    return "\t {}: {}, avg={}, min={}, max={}".format(
        db,
        timedelta(microseconds=sum(res)),
        timedelta(microseconds=sum(res) / size),
        timedelta(microseconds=min(res)),
        timedelta(microseconds=max(res))
    )


def test_bookmarks(cassandra: TestCassandra, mongo: TestMongo):
    print(f"Test reading {settings.bookmarks_count} bookmarks:")

    bookmarks = []
    for i in range(settings.bookmarks_count):
        bookmarks.append((uuid4(), uuid4()))

    res = cassandra.bookmarks(bookmarks)
    print(res_format('cassandra', res, len(bookmarks)))
    res = mongo.bookmarks(bookmarks)
    print(res_format('mongo', res, len(bookmarks)))


def test_likes(cassandra: TestCassandra, mongo: TestMongo):
    likes = []
    film_ids = [uuid4() for _ in range(int(log(settings.likes_count, 1.001)))]

    print(f"Test average rating of {len(film_ids)} films in {settings.likes_count} likes:")

    for _ in range(settings.likes_count):
        likes.append((
            choice(film_ids),
            uuid4(),
            randint(0, 10)
        ))

    res = cassandra.likes(likes, film_ids)
    print(res_format('cassandra', res, len(film_ids)))
    res = mongo.likes(likes, film_ids)
    print(res_format('mongo', res, len(film_ids)))


def test_likes_insert(cassandra: TestCassandra, mongo: TestMongo):
    likes = []
    film_ids = [uuid4() for _ in range(int(log(settings.likes_count, 1.001)))]

    print(f"Test insert data and read average rating of {len(film_ids)} films in {settings.likes_count} likes:")

    for _ in range(settings.likes_count):
        likes.append((
            choice(film_ids),
            uuid4(),
            randint(0, 10)
        ))

    res = cassandra.likes_insert(likes)
    print(res_format('cassandra', res, len(likes)))
    res = mongo.likes_insert(likes)
    print(res_format('mongo', res, len(likes)))


def start():
    cassandra = TestCassandra()
    mongo = TestMongo()

    test_bookmarks(cassandra, mongo)
    test_likes(cassandra, mongo)
    test_likes_insert(cassandra, mongo)

    cassandra.close()
    mongo.close()


if __name__ == '__main__':
    start()
