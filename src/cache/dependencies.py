
import json
from src.games.repositories import GameRepository
from src.providers.repositories import ProviderRepository


from .cache import redis_client
from .services import GameSearchService
from .services import ProviderSearchService


def game_service():
    return GameSearchService(GameRepository)


def provider_service():
    return ProviderSearchService(ProviderRepository)


async def add_cache(query, data):
    await redis_client.setex(query, 100, data)


async def data_to_json(data):
    data = [dict(row.to_read_model()) for row in data]
    json_data = json.dumps(data)
    return json_data


async def cache_service(query):
    if query:
        redis_query = await redis_client.get(query)
        if redis_query:
            cache = json.loads(redis_query)
            print(f"cache = {cache}, type = {type(cache)}")
            return cache
    return query
