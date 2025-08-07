
from fastapi import APIRouter

from src.database import SessionDep
from .cache import redis_client
from .cache import check_chache
from .search import search_client


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
async def search(session: SessionDep, query: str):
    print(f"=== START ===")
    if query:
        # cache = await check_chache(query)
        # if cache:
        #     return {
        #         "success": True,
        #         "msg": "Cache has been finded",
        #         "cache": cache
        #     }

        await search_client.search(query, session)

        json_res = await search_client.get_all_game(session)

        if not json_res:
            json_res = await search_client.get_all_provider(session)

        if json_res:
            await redis_client.setex(query, 1000, json_res)
            return {
                "success": True,
                "msg": "Query has been cached",
                "json_res": json_res
            }
    return {
        "success": False,
        "msg": "Enter some query",
        "query": query
    }
