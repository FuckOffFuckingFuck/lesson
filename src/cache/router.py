
from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends

from .dependencies import game_service
from .dependencies import provider_service
from .dependencies import add_cache
from .dependencies import cache_service
from .dependencies import data_to_json
from .services import GameSearchService
from .services import ProviderSearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
async def search(
    provider_service: Annotated[ProviderSearchService, Depends(provider_service)],
    game_service: Annotated[GameSearchService, Depends(game_service)],
    query: str = Depends(cache_service)
):
    if isinstance(query, list):
        return {
            "success": True,
            "msg": "Cache has been finded",
            "json_res": query
        }
    if isinstance(query, str):
        game_data = await game_service.search(query)
        provider_data = await provider_service.search(query)
        data = game_data + provider_data
        json_data = await data_to_json(data)
        await add_cache(query, json_data)
        return {
            "success": True,
            "msg": "Query has been cached",
            "data": game_data + provider_data,
        }
    return {
        "success": False,
        "msg": "Enter some query",
        "query": query
    }
