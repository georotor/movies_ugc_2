from services.like import LikeService, get_like_service
from services.review import ReviewService, get_review_service
from db_managers.abstract_manager import AbstractDBManager
from models import Like, FilmViewModel
from functools import lru_cache
from fastapi import Depends
from db_managers.mongo import get_db_manager
from uuid import UUID
from pydantic import BaseModel


class FilmService:
    """Собираем всю информацию о фильме в одном месте. """

    def __init__(
            self, model: type(BaseModel),
            like: LikeService,
            review: ReviewService
    ):
        """Базовый конструктор класса.

        Args:
          model: модель Pydantic для валидации данных;
          like: сервис для работы с лайками;
          review: сервис для работы с обзорами;

        """
        self.model = model
        self.like = like
        self.review = review

    async def get_rating(self, film_id: UUID) -> dict:
        """Получаем разные метрики рейтинга.

        Args:
          film_id: id фильма для которого нужно посчитать рейтинг.

        """
        likes = await self.like.search(
            film_id=film_id, page_size=9999, page_number=1, sort='-date',
        )

        return {
            'recent_likes': [like for like in likes[:10]],
            'absolute_rating': sum([like.score for like in likes]),
            'average_rating': sum([like.score for like in likes])/len(likes),
            'likes': len([1 for like in likes if like.score == 10]),
            'dislikes': len([1 for like in likes if like.score == 0]),
        }

    async def get_review(self, film_id: UUID) -> dict:
        """Получаем разные метрики рейтинга.

        Args:
          film_id: id фильма для которого нужны обзоры.

        """
        reviews = await self.review.search(
            film_id=film_id, page_size=9999, page_number=1, sort='-date',
        )

        return {
            'recent_reviews': [review for review in reviews[:10]],
        }


@lru_cache()
def get_film_service(
        like: LikeService = Depends(get_like_service),
        review: ReviewService = Depends(get_review_service)
):
    return FilmService(
        model=FilmViewModel, like=like, review=review,
    )
