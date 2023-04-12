"""Модели для валидации данных базовых UGC объектов."""
from datetime import datetime
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(row_data, *, default):
    """Функция для дампа в ORJSON.

    Args:
        row_data: данные для дампа;
        default: функция-сериалайзер по умолчанию.

    Returns:
        JSON дамп.

    """
    return orjson.dumps(row_data, default=default).decode()


class ORJSONBaseModel(BaseModel):
    """Базовая модель с измененным сериализатором."""

    class Config:
        """Используем ORJSON для лучшей производительности."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UGCModel(ORJSONBaseModel):
    """Базовая модель UGCModel.

    Во всех пользовательских данных практически всегда будет ссылка на
    пользователя (автора) и объект (фильм) к которому они относятся.

    """

    user_id: UUID
    obj_id: UUID
    date: datetime


class Bookmark(UGCModel):
    """Закладки (место окончания просмотра фильма).

    Возможна ситуация, когда пользователь добавил фильм в закладки еще до
    начала просмотра. Поэтому временная метка по умолчанию равна нулю.

    """

    timestamp: int = 0


class Review(UGCModel):
    """Рецензия на фильм. Состоит из заглавия и тела рецензии."""

    title: str
    text: str


class Like(UGCModel):
    """Оценка фильму - лайк (10) или дизлайк (0)."""

    score: int = 10
