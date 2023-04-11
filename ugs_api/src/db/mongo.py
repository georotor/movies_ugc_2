from motor.motor_asyncio import AsyncIOMotorClient
from settings import settings

mongo: AsyncIOMotorClient | None = None


def get_mongo() -> AsyncIOMotorClient:
    mongo = AsyncIOMotorClient(settings.MONGO_HOST, settings.MONGO_PORT)
    return mongo
