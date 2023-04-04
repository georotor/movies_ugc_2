import random
from datetime import datetime

from pymongo import MongoClient

from config import settings


class TestMongo:
    def __init__(self):
        self.client = MongoClient(settings.mongo_host, settings.mongo_port)
        self.db = self.client.research

        self.db.bookmarks.create_index("user_id", unique=True, sparse=True)
        self.db.likes.create_index("film_id", sparse=True)

    def close(self):
        self.client.drop_database('research')
        self.client.close()

    def bookmarks(self, data: list) -> list:
        collection = self.db.bookmarks

        collection.insert_many([
            {
                'user_id': str(user_id),
                'film_ids': [str(film_id)]
            } for user_id, film_id in data
        ])

        res = []

        for _ in range(settings.bookmarks_count):
            start = datetime.now()

            user_id, film_id = random.choice(data)
            collection.find_one({'user_id': str(user_id)})

            end = datetime.now()
            res.append((end - start).microseconds)

        return res

    def likes(self, data: list, film_ids: list) -> list:
        collection = self.db.likes

        collection.insert_many([
            {
                'film_id': str(film_id),
                'user_id': str(user_id),
                'score': score
            } for film_id, user_id, score in data
        ])

        res = []

        for film_id in film_ids:
            pipeline = [
                {'$match': {
                    'film_id': str(film_id)
                }},
                {'$group': {
                    '_id': None,
                    'avgscore': {'$avg': '$score'}
                }}
            ]

            start = datetime.now()

            for _ in collection.aggregate(pipeline):
                pass

            end = datetime.now()
            res.append((end - start).microseconds)

        return res

    def likes_insert(self, data: list) -> list:
        collection = self.db.likes

        res = []

        for film_id, user_id, score in data:
            pipeline = [
                {'$match': {
                    'film_id': str(film_id)
                }},
                {'$group': {
                    '_id': None,
                    'avgscore': {'$avg': '$score'}
                }}
            ]

            start = datetime.now()

            collection.insert_one({
                'film_id': str(film_id),
                'user_id': str(user_id),
                'score': score
            })

            for _ in collection.aggregate(pipeline):
                pass

            end = datetime.now()
            res.append((end - start).microseconds)

        return res
