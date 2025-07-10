
import uvicorn
from fastapi import FastAPI

from database import SessionDep  # fix "testdatabase" to "database"
from cache import redis_client
from service import check_chache
from search import search_client

app = FastAPI()


@app.get("/search", tags=["Search"])
async def search(session: SessionDep, query: str | None):
    if query:
        cache = await check_chache(query)
        if cache:
            return {
                "success": True,
                "msg": "Cache has been finded",
                "cache": cache
            }

        await search_client.search(query, session)

        json_res = await search_client.get_first_game(session)

        if not json_res:
            json_res = await search_client.get_first_provider(session)

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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
