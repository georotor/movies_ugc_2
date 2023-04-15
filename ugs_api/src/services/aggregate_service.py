"""Сервис для сбора информации из нескольких таблиц (коллекций)."""
from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from models.aggregate_models import FilmAggregateModel, ReviewAggregateDetailModel, UserResponseModel
from services.ugc.bookmark import BookmarkService, get_bookmark_service
from services.ugc.like import LikeService, get_like_service, get_review_like_service
from services.ugc.review import ReviewService, get_review_service

MAX_PAGE_SIZE = 9999


class AggregateService:
    """Сервис для сбора информации из нескольких таблиц (коллекций)."""

    def __init__(
        self,
        model: type(BaseModel),
        like: LikeService,
        review: ReviewService,
        bookmark: BookmarkService,
    ):
        """Базовый конструктор класса.

        Args:
          model: модель Pydantic для валидации данных;
          like: сервис для работы с лайками;
          review: сервис для работы с обзорами;
          bookmark: сервис для работы с закладками.

        """
        self.model = model
        self.like = like
        self.review = review
        self.bookmark = bookmark

    async def get_rating(self, obj_id: UUID) -> dict:
        """Получаем разные метрики рейтинга.

        Args:
          obj_id: id объекта для которого нужно посчитать рейтинг.

        """
        likes = await self.like.search(
            obj_id=obj_id,
            page_size=MAX_PAGE_SIZE,
            page_number=1,
            sort='-date',
        )
        scores = [like.score for like in likes]
        return {
            'recent_likes': likes[:10],
            'absolute_rating': sum(scores) if scores else None,
            'average_rating': (sum(scores) / len(likes)) if scores else None,
            'likes': len([1 for like in likes if like.score == 10]),
            'dislikes': len([1 for like in likes if like.score == 0]),
        }


@lru_cache()
def get_film_aggregate_service(
    like: LikeService = Depends(get_like_service),
    review: ReviewService = Depends(get_review_service),
    bookmark: BookmarkService = Depends(get_bookmark_service),
):
    """DI для FastAPI. Возвращает сервис для работы с фильмами."""
    return AggregateService(
        model=FilmAggregateModel,
        like=like,
        review=review,
        bookmark=bookmark,
    )


@lru_cache()
def get_review_aggregate_service(
    like: LikeService = Depends(get_review_like_service),
    review: ReviewService = Depends(get_review_service),
    bookmark: BookmarkService = Depends(get_bookmark_service),
):
    """DI для FastAPI. Возвращает сервис для работы с обзорами."""
    return AggregateService(
        model=ReviewAggregateDetailModel, like=like, review=review, bookmark=bookmark,
    )


@lru_cache()
def get_user_aggregate_service(
    like: LikeService = Depends(get_like_service),
    review: ReviewService = Depends(get_review_service),
    bookmark: BookmarkService = Depends(get_bookmark_service),
):
    """DI для FastAPI. Возвращает сервис для работы с обзорами."""
    return AggregateService(
        model=UserResponseModel,
        like=like,
        review=review,
        bookmark=bookmark,
    )
