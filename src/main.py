
import uvicorn
from fastapi import FastAPI

from database import SessionDep
from cache import redis_client
from service import check_chache
from search import search_client

# Импорты для тестовых ручек
# from models import Game
# from models import Provider
# from schemas import GameCreate
# from schemas import ProviderCreate


app = FastAPI()


@app.get("/search", tags=["Search"])
async def search(session: SessionDep, query: str):
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

# ручки для добавления данных в БД

# @app.post("/providers/", tags=["Provider"])
# async def create_provider(data: ProviderCreate, session: SessionDep):
#     db_provider = Provider(name=data.name, email=data.email)
#     session.add(db_provider)
#     await session.commit()
#     return {"succses": True, "send": db_provider}


# @app.get("/providers/{provider_id}", tags=["Provider"])
# async def read_provider(provider_id: int, session: SessionDep):
#     provider = await session.get(Provider, provider_id)
#     return {"succses": True, "id": provider_id, "send": provider}


# @app.post("/games/", tags=["Game"])
# async def create_game(data: GameCreate, session: SessionDep):
#     db_game = Game(
#         title=data.title,
#         price=data.price,
#         provider_id=data.provider_id
#     )
#     session.add(db_game)
#     await session.commit()
#     return {"succses": True, "send": db_game}


# @app.get("/games/{game_id}", tags=["Game"])
# async def read_game(game_id: int, session: SessionDep):
#     game = await session.get(Game, game_id)
#     return {"succses": True, "id": game_id, "send": game}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
