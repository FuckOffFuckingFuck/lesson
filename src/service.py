import json

from cache import redis_client


async def check_chache(query):
    if query:
        redis_query = await redis_client.get(query)
        if redis_query:
            pass
            cached_result = json.loads(redis_query)
            return cached_result
    return None
