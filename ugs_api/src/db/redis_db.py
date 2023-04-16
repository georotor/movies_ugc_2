"""DI для подключения к Redis."""

from redis.asyncio.client import Redis


client: Redis | None = None


async def get_redis() -> Redis | None:
    """DI для подключения к Redis."""
    return client
