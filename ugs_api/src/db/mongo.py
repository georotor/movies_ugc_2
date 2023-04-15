"""DI для базы подключения к MongoDB."""
from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings

mongo: AsyncIOMotorClient | None = None


def get_mongo() -> AsyncIOMotorClient:
    """DI для базы подключения к MongoDB."""
    return AsyncIOMotorClient(settings.MONGO_HOST, settings.MONGO_PORT)
