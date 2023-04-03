from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_host: str = '127.0.0.1'
    mongo_port: int = 27017

    cassandra_host: str = '127.0.0.1'

    bookmarks_count: int = 100000
    likes_count: int = 100000


settings = Settings()
