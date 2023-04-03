from uuid import uuid4
from math import log
from random import choice, randint

from config import settings
from db.cassandradb import TestCassandra
from db.mongodb import TestMongo


def test_bookmarks(cassandra: TestCassandra, mongo: TestMongo):
    print(f"Test reading {settings.bookmarks_count} bookmarks:")

    bookmarks = []
    for i in range(settings.bookmarks_count):
        bookmarks.append((uuid4(), uuid4()))

    time_all = cassandra.bookmarks(bookmarks)
    print("\t cassandra: {0}, per one = {1}".format(time_all, time_all / settings.bookmarks_count))
    time_all = mongo.bookmarks(bookmarks)
    print("\t mongo: {0}, per one = {1}".format(time_all, time_all / settings.bookmarks_count))


def test_likes(cassandra: TestCassandra, mongo: TestMongo):
    likes = []
    film_ids = [uuid4() for _ in range(int(log(settings.likes_count, 1.001)))]

    print(f"Test average rating of {len(film_ids)} films and {settings.likes_count} likes:")

    for _ in range(settings.likes_count):
        likes.append((
            choice(film_ids),
            uuid4(),
            randint(0, 10)
        ))

    time_all = cassandra.likes(likes, film_ids)
    print("\t cassandra: {0}, per one = {1}".format(time_all, time_all / settings.likes_count))
    time_all = mongo.likes(likes, film_ids)
    print("\t mongo: {0}, per one = {1}".format(time_all, time_all / settings.likes_count))


def start():
    cassandra = TestCassandra()
    mongo = TestMongo()

    test_bookmarks(cassandra, mongo)
    test_likes(cassandra, mongo)

    cassandra.close()
    mongo.close()


if __name__ == '__main__':
    start()
