"""Реализация AbstractDBManager для MongoDB."""
from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_mongo
from db_managers.abstract_manager import AbstractDBManager
from settings import settings


class MongoManager(AbstractDBManager):
    """Реализация AbstractDBManager для MongoDB."""

    def __init__(self, client, db_name):
        """Конструктор класса.

        Args:
            client: инициированное подключение к БД;
            db_name: название БД.

        """
        self.db = client[db_name]

    async def search(
        self, table: str, search: dict, limit: int, offset: int, sort: list,
    ):
        """Поиск, возвращающий список значений.

        Args:
          table: название таблицы (коллекции) БД;
          search: словарь с данными для поиска;
          limit: кол-во элементов в выдаче;
          offset: смещение (пропуск первых N элементов);
          sort: список полей и направлений сортировки [(id, 1), (name, -1)].

        """
        collection = self._open_collection(table)
        cursor = collection.find(search).skip(offset).limit(limit)
        return await cursor.sort(sort).to_list(length=limit)

    async def get(self, table: str, search: dict):
        """Поиск, возвращающий только одно значение.

        Args:
          table: название таблицы (коллекции) БД;
          search: словарь с данными для поиска.

        """
        collection = self._open_collection(table)
        return await collection.find_one(search)

    async def create(self, table: str, obj_data: dict):
        """Создание записи в БД.

        Args:
          table: название таблицы (коллекции) БД;
          obj_data: словарь с данными для поиска.

        """
        collection = self._open_collection(table)
        await collection.insert_one(obj_data)

    async def delete(self, table: str, search: dict):
        """Удаление записи из БД.

        Args:
          table: название таблицы (коллекции) БД;
          search: словарь с данными для поиска.

        """
        collection = self._open_collection(table)
        await collection.delete_many(search)

    def aggregate(
        self,
            table: str,
            search: dict,
            related_table: str,
            related_fields: list,
            desired_property: str,
            limit: int,
            offset: int,
            sort: list,
    ):
        """Создание запроса для агрегирования данных.

        Объединяет две таблицы (коллекции) на основе двух связанных полей.
        Создает поля со средним и суммарным значением искомого атрибута.
        Добавляет поля "avg" и "sum" которые можно использовать для сортировки.
        Пример: добавляет рейтинг и среднюю оценку и обзору.

        Args:
          table: название таблицы (коллекции) БД;
          search: словарь с данными для поиска;
          related_table: название связанной таблицы (коллекции) БД;
          related_fields: названия связанных полей локального и внешнего объекта;
          desired_property: искомый атрибут у связанного объекта;
          limit: кол-во элементов в выдаче;
          offset: смещение (пропуск первых N элементов);
          sort: список полей и направление сортировки [('avg', 1)].

        """
        collection = self._open_collection(table)
        lookup = {
            'from': related_table,
            'localField': related_fields[0],
            'foreignField': related_fields[1],
            'as': 'related_object',
        }
        avg_filed = {'$avg': '$related_object.{0}'.format(desired_property)}
        sum_field = {'$sum': '$related_object.{0}'.format(desired_property)}
        return collection.aggregate(
            [
                {'$match': search},
                {'$lookup': lookup},
                {'$addFields': {'avg': avg_filed, 'sum': sum_field}},
                {'$sort': {sort[0]: sort[1]}},
                {'$skip': offset},
                {'$limit': limit},
            ],
        ).to_list(length=limit)

    def _open_collection(self, collection_name: str):
        """Переходим к нужной коллекции."""
        return self.db[collection_name]


@lru_cache
def get_db_manager(
    client: AsyncIOMotorClient = Depends(get_mongo),
) -> AbstractDBManager:
    """DI для FastAPI. Получаем менеджер для MONGO."""
    return MongoManager(client=client, db_name=settings.MONGO_DB_NAME)
