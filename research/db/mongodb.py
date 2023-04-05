"""Модуль с тестами для Mongo."""
import random
from datetime import datetime

from pymongo import MongoClient

from config import settings


class TestMongo:
    """Класс с тестами для Mongo."""

    def __init__(self):
        """Подключение к БД и создание индексов."""
        self.client = MongoClient(settings.mongo_host, settings.mongo_port)
        self.db = self.client.research

        self.db.bookmarks.create_index('user_id', unique=True, sparse=True)
        self.db.likes.create_index('film_id', sparse=True)

    def close(self):
        """Очистка БД и закрытие соединения."""
        self.client.drop_database('research')
        self.client.close()

    def bookmarks(self, bookmarks_data: list) -> list:
        """Тесты на чтение закладок."""
        self.db.bookmarks.insert_many([
            {
                'user_id': str(user_id),
                'film_ids': [str(film_id)],
            } for user_id, film_id in bookmarks_data
        ])

        res = []

        for _ in range(settings.bookmarks_count):
            start = datetime.now()

            user_id, film_id = random.choice(bookmarks_data)
            self.db.bookmarks.find_one({'user_id': str(user_id)})

            res.append((datetime.now() - start).microseconds)

        return res

    def likes(self, likes_data: list, film_ids: list) -> list:
        """Тесты на чтение средней оценки кинопроизведения."""
        self.db.likes.insert_many([
            {
                'film_id': str(film_id),
                'user_id': str(user_id),
                'score': score,
            } for film_id, user_id, score in likes_data
        ])

        res = []

        for film_id in film_ids:
            pipeline = [
                {'$match': {
                    'film_id': str(film_id),
                }},
                {'$group': {
                    '_id': None,
                    'avgscore': {'$avg': '$score'},
                }},
            ]

            start = datetime.now()

            for _ in self.db.likes.aggregate(pipeline):
                pass

            res.append((datetime.now() - start).microseconds)

        return res

    def likes_insert(self, likes_data: list) -> list:
        """Тесты на скорость записи лайков и последующем чтении средней оценки фильма."""
        res = []

        for film_id, user_id, score in likes_data:
            pipeline = [
                {'$match': {
                    'film_id': str(film_id),
                }},
                {'$group': {
                    '_id': None,
                    'avgscore': {'$avg': '$score'},
                }},
            ]

            start = datetime.now()

            self.db.likes.insert_one({
                'film_id': str(film_id),
                'user_id': str(user_id),
                'score': score,
            })

            for _ in self.db.likes.aggregate(pipeline):
                pass

            res.append((datetime.now() - start).microseconds)

        return res
