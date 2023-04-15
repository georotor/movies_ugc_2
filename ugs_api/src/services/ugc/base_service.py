"""Базовые UGS сервисы и сопутствующие исключения."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from db_managers.abstract_manager import AbstractDBManager
from models.ugc_models import UGCModel

MAX_PAGE_SIZE = 9999


class UGSServiceError(Exception):
    """Базовое исключение для всех ошибок в работе AbstractService."""


class DocNotUniqueError(UGSServiceError):
    """Исключение при попытке создать дубль уникальной записи."""


class DocNotFoundError(UGSServiceError):
    """Исключение при попытке получить отсутствующую запись."""


class UGCService:
    """Базовый класс для UGS сервисов."""

    def __init__(
        self,
        model: type(UGCModel),
        db: AbstractDBManager,
        collection_name: str,
    ):
        """Базовый конструктор класса.

        Args:
          model: модель UGCModel (Pydantic) для валидации данных;
          db: инициализированный менеджер для работы с БД;
          collection_name: название таблицы (коллекции) БД.

        """
        self.model = model
        self.db = db
        self.collection_name = collection_name

    async def get(
        self,
        obj_id: UUID,
        user_id: UUID,
    ):
        """GET запрос для поиска данных. Возвращает только одно значение.

        Args:
          obj_id: идентификатор связанного объекта (фильма / обзора);
          user_id: идентификатор пользователя.

        """
        doc = await self.db.get(
            self.collection_name, self._create_search_query(obj_id, user_id),
        )
        if not doc:
            return None
        return self.model(**doc)

    async def search(
        self,
        obj_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        page_size: int = 10,
        page_number: int = 1,
        sort: str = '_id',
    ):
        """GET запрос для поиска данных. Возвращает несколько значений.

        Можно фильтровать запрос по пользователю или фильму.
        Поддерживается пагинация (LIMIT / OFFSET) и сортировку.

        Args:
          obj_id: идентификатор связанного объекта (фильма / обзора);
          user_id: идентификатор пользователя;
          page_size: кол-во данных на странице;
          page_number: номер страницы;
          sort: поле для сортировки, '-' означает обратный порядок сортировки.

        """
        search_query = self._create_search_query(obj_id, user_id)
        sort_order = -1 if sort.startswith('-') else 1
        docs = await self.db.search(
            self.collection_name,
            search_query,
            page_size,
            page_size * (page_number - 1),
            sort=[(sort.lstrip('-'), sort_order)],
        )
        if not docs:
            return []
        return [self.model(**doc) for doc in docs]

    async def create(
        self,
        obj_id: UUID,
        user_id: UUID,
        **kwargs,
    ):
        """CREATE запрос для создания данных.

        Если у этого пользователя для этого фильма уже была создана запись,
        то заменяем старую на новую.

        Args:
          obj_id: идентификатор связанного объекта (фильма / обзора);
          user_id: идентификатор пользователя,
          kwargs: дополнительные данные объекта.

        """
        if await self.get(obj_id, user_id) is not None:
            await self.delete(obj_id, user_id)

        search_query = self._create_search_query(obj_id, user_id)
        search_query.update(kwargs)
        search_query['date'] = datetime.now()
        await self.db.create(self.collection_name, search_query)

    async def delete(self, obj_id: Optional[UUID] = None, user_id: Optional[UUID] = None):
        """DELETE запрос для удаления данных.

        На данным этапе считаем, что связка "пользователь + фильм" уникальна и
        ничего лишнего мы не удалим. Можно добавить проверку на наличие записи,
        но это лишний запрос в БД:

        if not await self.get(obj_id, user_id):
            raise DocNotFoundError('Запись не существует')

        Args:
          obj_id: идентификатор связанного объекта (фильма / обзора);
          user_id: идентификатор пользователя.

        """
        search_query = self._create_search_query(obj_id, user_id)
        await self.db.delete(self.collection_name, search_query)

    async def aggregate(
        self,
        related_table: str,
        related_fields: list,
        desired_property: str,
        obj_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        page_size: int = 10,
        page_number: int = 1,
        sort: str = '-avg',
    ):
        """GET запрос для агрегирования данных из нескольких таблиц (коллекций).

        Поддерживается пагинация (LIMIT / OFFSET) и сортировку.
        Добавляет свойства "avg" и "sum" по которым также можно сортировать.

        Args:
          related_table: имя связанной таблицы (коллекции);
          related_fields: названия связанных полей локального и внешнего объекта;
          desired_property: название искомого поле, по которому будет считаться
          среднее и суммарное значение;
          obj_id: идентификатор связанного объекта (фильма / обзора);
          user_id: идентификатор пользователя;
          page_size: кол-во данных на странице;
          page_number: номер страницы;
          sort: поле для сортировки, '-' означает обратный порядок сортировки.

        """
        search_query = self._create_search_query(obj_id, user_id)
        sort_order = -1 if sort.startswith('-') else 1
        return await self.db.aggregate(
            self.collection_name,
            search_query,
            related_table,
            related_fields,
            desired_property,
            page_size,
            page_size * (page_number - 1),
            sort=[sort.lstrip('-'), sort_order],
        )

    def _create_search_query(self, obj_id, user_id):
        """Для простоты конвертации в bson приводим UUID к строке.

        Альтернатива - bson.Binary.from_uuid().

        Args:
          obj_id: идентификатор связанного объекта (фильма / обзора);
          user_id: идентификатор пользователя.

        """
        query = {}
        if obj_id:
            query['obj_id'] = str(obj_id)
        if user_id:
            query['user_id'] = str(user_id)
        return query
