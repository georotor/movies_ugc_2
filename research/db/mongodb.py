import random
from datetime import datetime, timedelta

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

    def bookmarks(self, data: list) -> timedelta:
        collection = self.db.bookmarks

        collection.insert_many([
            {
                'user_id': str(user_id),
                'film_ids': [str(film_id)]
            } for user_id, film_id in data
        ])

        start = datetime.now()
        for _ in range(settings.bookmarks_count):
            user_id, film_id = random.choice(data)
            collection.find_one({'user_id': str(user_id)})
        end = datetime.now()

        return end - start

    def likes(self, data: list, film_ids: list) -> timedelta:
        collection = self.db.likes

        collection.insert_many([
            {
                'film_id': str(film_id),
                'user_id': str(user_id),
                'score': score
            } for film_id, user_id, score in data
        ])

        start = datetime.now()
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

            for _ in collection.aggregate(pipeline):
                pass
        end = datetime.now()

        return end - start
