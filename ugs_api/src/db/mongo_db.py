"""DI для базы подключения к MongoDB."""
from motor.motor_asyncio import AsyncIOMotorClient

mongo: AsyncIOMotorClient | None = None


def get_mongo() -> AsyncIOMotorClient:
    """DI для базы подключения к MongoDB."""
    return mongo
