"""Модели для валидации данных FastAPI."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from models.base_model import ORJSONBaseModel


class UGCModel(ORJSONBaseModel):
    """Базовая модель UGCModel.

    Во всех пользовательских данных практически всегда будет ссылка на
    пользователя (автора) и объект (фильм) к которому они относятся.

    """

    user_id: UUID
    film_id: UUID
    date: datetime


class Bookmark(UGCModel):
    """Закладки (место окончания просмотра фильма).

    Возможна ситуация, когда пользователь добавил фильм в закладки еще до
    начала просмотра. Поэтому временная метка по умолчанию равна нулю.

    """

    timestamp: int = 0


class Like(UGCModel):
    """Оценка фильму - лайк (10) или дизлайк (0)."""

    score: int = 10


class Review(UGCModel):
    """Рецензия на фильм. Состоит из заглавия и тела рецензии."""

    title: str
    text: str


class ReviewLike(ORJSONBaseModel):
    """Лайк для ревью. Заменяем поле film_id на review_id."""

    user_id: UUID
    review_id: UUID
    date: datetime


class FilmViewModel(ORJSONBaseModel):
    """Общая информация и фильме: лайки, рейтинг, рецензии и пр."""

    film_id: UUID
    recent_likes: list[Optional[Like]]
    absolute_rating: int
    average_rating: float
    likes: int
    dislikes: int
    recent_reviews: list[Optional[Review]]
