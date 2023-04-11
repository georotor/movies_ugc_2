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

    def _open_collection(self, collection_name: str):
        """Переходим к нужной коллекции."""
        return self.db[collection_name]


@lru_cache
def get_db_manager(
    client: AsyncIOMotorClient = Depends(get_mongo),
) -> AbstractDBManager:
    """DI для FastAPI."""
    return MongoManager(client=client, db_name=settings.MONGO_DB_NAME)
