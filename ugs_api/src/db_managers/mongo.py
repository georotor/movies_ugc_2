from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from db_managers.abstract_manager import AbstractDBManager, DBManagerError
from db.mongo import get_mongo
from settings import settings
from functools import lru_cache


class MongoManager(AbstractDBManager):
    def __init__(self, client, db_name):
        self.db = client[db_name]

    def _open_collection(self, collection_name: str):
        """Переходим к нужной коллекции. """
        return self.db[collection_name]

    async def search(
            self, table: str, data: dict, limit: int, offset: int, sort: list,
    ):
        """Поиск, возвращающий список значений.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска;
          limit: кол-во элементов в выдаче;
          offset: смещение (пропуск первых N элементов);
          sort: список полей и направлений сортировки [(id, 1), (name, -1)].

        """
        collection = self._open_collection(table)
        cursor = collection.find(data).skip(offset).limit(limit).sort(sort)
        return await cursor.to_list(length=limit)

    async def get(self, table: str, data: dict):
        """Поиск, возвращающий только одно значение.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска.

        """
        collection = self._open_collection(table)
        return await collection.find_one(data)

    async def create(self, table: str, data: dict):
        """Создание записи в БД.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска.

        """
        collection = self._open_collection(table)
        await collection.insert_one(data)

    async def delete(self, table: str, data: dict):
        """Удаление записи из БД.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска.

        """
        collection = self._open_collection(table)
        await collection.delete_many(data)


@lru_cache
def get_db_manager(client: AsyncIOMotorClient = Depends(get_mongo)) -> AbstractDBManager:
    db_manager = MongoManager(client=client, db_name=settings.MONGO_DB_NAME)
    return db_manager
