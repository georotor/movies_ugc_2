import orjson as orjson
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ORJSONBaseModel(BaseModel):
    """Как и в прошлых спринтах будет использовать более ORJSON, что даст
    преимущество в скорости сереализации данных.

    """
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UGSModel(ORJSONBaseModel):
    """Во всех пользовательских данных всегда будет ссылка на пользователя
    (автора) и объект (фильм) к которому они относятся.

    """
    user_id: UUID
    film_id: UUID
    date: datetime


class Bookmark(UGSModel):
    """Возможна ситуация, когда пользователь добавил фильм в закладки еще до
    начала просмотра. Поэтому временная метка по умолчанию равна нулю.

    """
    timestamp: int = 0


class Like(UGSModel):
    """Лайк или дизлайк объекту (фильму / рецензии). Лайк оцениваем в 10,
    дизлайк - в 0.

    """
    score: int = 10


class Review(UGSModel):
    """Рецензия на фильм. Состоит из заглавия и тела рецензии. """
    title: str
    text: str


class ReviewLike(ORJSONBaseModel):
    """Лайк для ревью. Заменяем поле film_id на review_id. """
    user_id: UUID
    review_id: UUID
    date: datetime


class FilmViewModel(ORJSONBaseModel):
    film_id: UUID
    recent_likes: list[Optional[Like]]
    absolute_rating: int
    average_rating: float
    likes: int
    dislikes: int
    recent_reviews: list[Optional[Review]]