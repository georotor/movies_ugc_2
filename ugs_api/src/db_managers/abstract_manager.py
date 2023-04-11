"""Описание интерфейса для работы с БД."""
from abc import ABC, abstractmethod


class DBManagerError(Exception):
    """Базовое исключение для ошибок в работе менеджера БД."""


class AbstractDBManager(ABC):
    """Простой менеджер для работы с БД."""

    @abstractmethod
    async def search(
        self, table: str, search: dict, limit: int, offset: int, sort: list,
    ):
        """Поиск, возвращающий список значений.

        Args:
          table: название таблицы (коллекции) БД;
          search: словарь с данными для поиска;
          limit: кол-во элементов в выдаче;
          offset: смещение (пропуск первых N элементов);
          sort: список с полями для сортировки.

        """

    @abstractmethod
    async def get(self, table: str, search: dict):
        """Поиск, возвращающий только одно значение.

        Args:
          table: название таблицы (коллекции) БД;
          search: словарь с данными для поиска.

        """

    @abstractmethod
    async def create(self, table: str, obj_data: dict):
        """Создание записи в БД.

        Args:
          table: название таблицы (коллекции) БД;
          obj_data: словарь с данными для поиска.

        """

    @abstractmethod
    async def delete(self, table: str, search: dict):
        """Удаление записи из БД.

        Args:
          table: название таблицы (коллекции) БД;
          search: словарь с данными для поиска.

        """
