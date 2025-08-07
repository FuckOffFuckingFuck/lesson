
import redis.asyncio as redis

from src.config import settings


class RedisCache:

    def __init__(self):
        self._cache = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0
        )  # docker redis

    async def get(self, key):
        return await self._cache.get(key)

    async def set(self, key, value):
        await self._cache.set(key, value)

    async def setex(self, key, ttl: int, value):
        await self._cache.setex(key, ttl, value)


redis_client = RedisCache()
