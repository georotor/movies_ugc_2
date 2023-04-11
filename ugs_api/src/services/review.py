from services.base_service import UGSService
from db_managers.abstract_manager import AbstractDBManager
from models import Review
from functools import lru_cache
from fastapi import Depends
from db_managers.mongo import get_db_manager
from typing import Optional
from uuid import UUID


class ReviewService(UGSService):
    """Переопределяем метод create, добавляя поля title и text. """
    def create(
            self,
            film_id: UUID,
            user_id: UUID,
            title: str = '',
            text: str = '',
    ):
        return super().create(film_id, user_id, title=title, text=text)


@lru_cache()
def get_review_service(db: AbstractDBManager = Depends(get_db_manager)):
    return ReviewService(model=Review, db=db, collection_name='review')
