"""Модели для валидации данных ответа FastAPI.

Включают в себя информацию из нескольких таблицы (коллекций) БД.

"""
from typing import Optional
from uuid import UUID

from models.ugc_models import Bookmark, Like, ORJSONBaseModel, Review


class FilmAggregateModel(ORJSONBaseModel):
    """Общая информация и фильме: лайки, рейтинг, рецензии и пр."""

    film_id: UUID
    recent_likes: Optional[list[Like]]
    absolute_rating: Optional[int]
    average_rating: Optional[float]
    likes: Optional[int]
    dislikes: Optional[int]
    recent_reviews: list[Optional[Review]]
    bookmark: Optional[Bookmark]


class ReviewAggregateDetailModel(ORJSONBaseModel):
    """Детальная информация об обзоре фильма.

    Заголовок и текст рецензии, авторская оценка фильма. Ссылка на фильм и
    пользователя. Рейтинг обзора.

    """

    review_id: UUID
    title: str
    text: str
    film_score: Optional[int]
    film_id: UUID
    user_id: UUID
    recent_likes: Optional[list[Like]]
    absolute_rating: Optional[int]
    average_rating: Optional[float]
    likes: Optional[int]
    dislikes: Optional[int]


class ReviewAggregateBriefModel(ORJSONBaseModel):
    """Детальная информация об обзоре фильма.

    Заголовок и текст рецензии, авторская оценка фильма. Ссылка на фильм и
    пользователя. Рейтинг обзора.

    """

    review_id: UUID
    title: str
    text: str
    film_id: UUID
    user_id: UUID
    absolute_rating: Optional[int]
    average_rating: Optional[float]


class UserResponseModel(ORJSONBaseModel):
    """Общая информация и пользователе: закладки, рецензии и пр."""

    user_id: UUID
    recent_likes: Optional[list[Like]]
    recent_reviews: Optional[list[Review]]
    bookmarks: Optional[list[Bookmark]]
