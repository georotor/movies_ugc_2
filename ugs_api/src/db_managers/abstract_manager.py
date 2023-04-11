from abc import ABC, abstractmethod


class DBManagerError(Exception):
    """Базовое исключение для ошибок в работе менеджера БД. """


class AbstractDBManager(ABC):
    """Простой менеджер для работы с БД. Предполагается, что все данные
    хранятся в одной таблице / коллекции и указывать ее название при каждом
    запросе не требуется.

    """
    @abstractmethod
    async def search(
            self, table: str, data: dict, limit: int, offset: int, sort: list,
    ):
        """Поиск, возвращающий список значений.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска;
          limit: кол-во элементов в выдаче;
          offset: смещение (пропуск первых N элементов);
          sort: список с полями для сортировки.

        """

    @abstractmethod
    async def get(self, table: str, data: dict):
        """Поиск, возвращающий только одно значение.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска.

        """

    @abstractmethod
    async def create(self, table: str, data: dict):
        """Создание записи в БД.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска.

        """

    @abstractmethod
    async def delete(self, table: str, data: dict):
        """Удаление записи из БД.

        Args:
          table: название таблицы (коллекции) БД;
          data: словарь с данными для поиска.

        """

