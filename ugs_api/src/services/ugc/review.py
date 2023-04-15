"""Сервис для обзоров (рецензий)."""
from functools import lru_cache
from uuid import UUID, uuid4

from fastapi import Depends

from db_managers.abstract_manager import AbstractDBManager
from db_managers.mongo import get_db_manager
from models.ugc_models import Review
from services.ugc.base_service import UGCService

MAX_PAGE_SIZE = 9999


class ReviewService(UGCService):
    """Сервис для обзоров (рецензий)."""

    def create(
        self,
        obj_id: UUID,
        user_id: UUID,
        title: str = '',
        text: str = '',
    ):
        """Переопределяем метод create, добавляя поля title и text."""
        return super().create(
            obj_id, user_id, title=title, text=text, review_id=str(uuid4()),
        )

    async def get_by_id(self, review_id: UUID):
        """GET запрос для поиска данных по id. Возвращает только одно значение.

        Args:
          review_id: идентификатор объекта.

        """
        doc = await self.db.get(
            self.collection_name, {'review_id': str(review_id)},
        )
        if not doc:
            return None
        return self.model(**doc)


@lru_cache()
def get_review_service(db: AbstractDBManager = Depends(get_db_manager)):
    """DI для FastAPI. Получаем сервис лайков для обзоров."""
    return ReviewService(model=Review, db=db, collection_name='review')
