import json

import redis.asyncio as redis

from src.config import settings


class RedisCache:

    def __init__(self):
        self.cache = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0
        )

    async def get(self, key):
        return await self.cache.get(key)

    async def set(self, key, value):
        await self.cache.set(key, value)

    async def setex(self, key, ttl: int, value):
        await self.cache.setex(key, ttl, value)


redis_client = RedisCache()


async def check_chache(query):
    if query:
        redis_query = await redis_client.get(query)
        if redis_query:
            pass
            cached_result = json.loads(redis_query)
            return cached_result
    return None
