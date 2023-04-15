"""Сервис для закладок пользователя."""
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db_managers.abstract_manager import AbstractDBManager
from db_managers.mongo import get_db_manager
from models.ugc_models import Bookmark
from services.ugc.base_service import UGCService


class BookmarkService(UGCService):
    """Сервис для закладок пользователя."""

    def create(
        self,
        obj_id: UUID,
        user_id: UUID,
        timestamp: int = 0,
    ):
        """Переопределяем метод create, добавляем timestamp."""
        return super().create(obj_id, user_id, timestamp=timestamp)


@lru_cache()
def get_bookmark_service(db: AbstractDBManager = Depends(get_db_manager)):
    """DI для FastAPI. Получаем сервис лайков для закладок."""
    return BookmarkService(model=Bookmark, db=db, collection_name='bookmarks')
