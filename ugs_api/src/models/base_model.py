"""Базовые модели с поддержкой ORJSON."""
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
