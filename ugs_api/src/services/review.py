"""Сервис для обзоров (рецензий)."""
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db_managers.abstract_manager import AbstractDBManager
from db_managers.mongo import get_db_manager
from models.ugc_models import Review
from services.base_service import UGCService


class ReviewService(UGCService):
    """Сервис для обзоров (рецензий)."""

    def create(
        self,
        film_id: UUID,
        user_id: UUID,
        title: str = '',
        text: str = '',
    ):
        """Переопределяем метод create, добавляя поля title и text."""
        return super().create(film_id, user_id, title=title, text=text)


@lru_cache()
def get_review_service(db: AbstractDBManager = Depends(get_db_manager)):
    """DI для FastAPI."""
    return ReviewService(model=Review, db=db, collection_name='review')
