from services.base_service import UGSService
from db_managers.abstract_manager import AbstractDBManager
from models import Like
from functools import lru_cache
from fastapi import Depends
from db_managers.mongo import get_db_manager
from uuid import UUID


class LikeService(UGSService):
    """Переопределяем метод create, добавляя поле score
    (лайк - 10, дизлайк - 0).

    """
    def create(
            self,
            film_id: UUID,
            user_id: UUID,
            score=10,
    ):
        return super().create(film_id, user_id, score=score)


@lru_cache()
def get_like_service(db: AbstractDBManager = Depends(get_db_manager)):
    return LikeService(model=Like, db=db, collection_name='like')
