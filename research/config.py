"""Настройки для тестирования производительности БД Mongo и Cassandra."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Класс настроек для тестирования производительности БД Mongo и Cassandra."""

    mongo_host: str = '127.0.0.1'
    mongo_port: int = 27017

    cassandra_host: str = '127.0.0.1'

    bookmarks_count: int = 100000
    likes_count: int = 100000
    films_count_factor: float = 1.001


settings = Settings()
