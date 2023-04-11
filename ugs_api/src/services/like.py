"""Сервис для лайктов / рейтинга."""
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db_managers.abstract_manager import AbstractDBManager
from db_managers.mongo import get_db_manager
from models.ugc_models import Like
from services.base_service import UGCService


class LikeService(UGCService):
    """Сервис для лайктов / рейтинга."""

    def create(
        self,
        film_id: UUID,
        user_id: UUID,
        score=10,
    ):
        """Переопределяем метод create, score для лайка - 10, для дизлайка - 0."""
        return super().create(film_id, user_id, score=score)


@lru_cache()
def get_like_service(db: AbstractDBManager = Depends(get_db_manager)):
    """DI для FastAPI."""
    return LikeService(model=Like, db=db, collection_name='like')
