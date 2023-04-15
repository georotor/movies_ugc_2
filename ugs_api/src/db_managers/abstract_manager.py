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

    @abstractmethod
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
