"""Config for fast api."""

from pydantic import BaseModel, BaseSettings


class Logging(BaseModel):
    """Основные уровни логирования."""

    level_root: str = 'INFO'
    level_uvicorn: str = 'INFO'
    level_console: str = 'DEBUG'


class Settings(BaseSettings):
    """Основные настройки проекта."""

    project_name = 'UGS API'
    request_id: bool = True
    redis_host: str = 'localhost'
    redis_port: int = 6379

    jwt_validate: bool = True
    auth_url: str = 'http://127.0.0.1:5000/api/v1/user/is_authenticated'
    cache_expire: int = 600

    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DB_NAME = 'ugc'
    DEFAULT_LIMIT = 10
    DEFAULT_OFFSET = 0

    sentry_dsn: str | None = None
    traces_sample_rate: float = 1.0

    logging: Logging = Logging()


settings = Settings()
