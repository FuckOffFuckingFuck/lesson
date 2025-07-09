import redis.asyncio as redis
from config import settings


class RedisCache:

    def __init__(self):
        self.redis = None

    async def init(self):
        self.redis = await redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=10
        )

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value):
        await self.redis.set(key, value)


redis_cache = RedisCache()

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)
