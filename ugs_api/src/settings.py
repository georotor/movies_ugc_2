"""Config for fast api kafka."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Основные настройки проекта."""

    project_name = 'UGS API'
    logger_api_url = 'http://127.0.0.1:5050/api/v1/'
    redis_host: str = 'localhost'
    redis_port: int = 6379

    jwt_validate: bool = True
    auth_url: str = 'http://127.0.0.1:5000/api/v1/user/is_authenticated'
    cache_expire: int = 600

    KAFKA_HOST: str = 'localhost'
    KAFKA_PORT: int = 9092
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DB_NAME = 'ugc'
    DEFAULT_LIMIT = 10
    DEFAULT_OFFSET = 0


settings = Settings()
