"""Config for fast api kafka."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Основные настройки проекта."""

    project_name = 'UGS API'
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DB_NAME = 'ugc'
    DEFAULT_LIMIT = 10
    DEFAULT_OFFSET = 0


settings = Settings()
