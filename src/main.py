
import uvicorn
from fastapi import FastAPI
from sqlalchemy import select

from testdatabase import SessionDep  # fix "testdatabase" to "database"
from models import Game
from models import Provider
from models import Base

import json
from cache import redis_cache, redis_client

from schemas import GameCreate
from schemas import ProviderCreate


app = FastAPI()


@app.get("/TEST_search", tags=["TEST"])
async def search(query: str | None, session: SessionDep):

    if query:
        redis_query = await redis_client.get(query)
        if redis_query:
            cached_result = json.loads(redis_query)
            # cached_result['cache'] = True
            return {"status": "OK: cache finded",
                    "redis_query": f"{redis_query}",
                    "cached_result": f"{cached_result}"}

        games_stmt = select(Game.id, Game.provider_id).where(
            Game.title.ilike(f"%{query}%"))
        games_result = await session.execute(games_stmt)
        game = [row[0] for row in games_result]

        if len(game) != 0:
            res = res = await session.get(Game, game[0])
            game = GameCreate(title=res.title,
                              price=res.price,
                              provider_id=res.provider_id)
            json_res = json.dumps(game)
            await redis_client.setex(query, 1000, json_res)
        else:
            provider_stmt = select(Provider.id).where(
                Provider.name.ilike(f"%{query}%"))
            provider_result = await session.execute(provider_stmt)
            provider = [row[0] for row in provider_result]
            res = await session.get(Provider, provider[0])
            provider = dict(ProviderCreate(name=res.name, email=res.email))
            json_res = json.dumps(provider)
            # print(f"========= cache added: json_res = {json_res}")
            await redis_client.setex(query, 1000, json_res)
    return {"OK": "query has been cached", "json_res": json_res}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


# @app.get("/TEST_search")
# async def search(query: str | None, session: SessionDep):

#     if query:
#         redis_query = await redis_client.get(query)
#         if redis_query:
#             # cached_result = json.loads(redis_query)
#             # cached_result['cache'] = True
#             return {"status": "OK: cache finded", "redis_query": f"{redis_query}"}

#         games_stmt = select(Game.id, Game.provider_id).where(
#             Game.title.ilike(f"%{query}%"))
#         games_result = await session.execute(games_stmt)
#         rows = games_result.all()
#         print(f"games rows = {rows}")

#         if not rows:
#             games = [row[0] for row in rows]

#             print(f"games = {games}")

#             provider_stmt = select(Provider.id).where(
#                 Provider.name.ilike(f"%{query}%"))
#             provider_result = await session.execute(provider_stmt)
#             provider_ids_from_name = [row[0] for row in provider_result]

#             provider = list(set(provider_ids_from_name))

#         await redis_client.setex(query, 1000, "append_cache")
#     return {"OK": True}


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


# @app.put("/providers/{provider_id}", tags=["Provider"])
# async def update_provider(provider_id: int, data: ProviderCreate, session: SessionDep):
#     db_provider = await session.get(Provider, provider_id)
#     db_provider.name = data.name
#     db_provider.email = data.email
#     await session.commit()
#     return {"succses": True, "id": provider_id, "send": db_provider}


# @app.delete("/providers/{provider_id}", tags=["Provider"])
# async def delete_provider(provider_id: int, session: SessionDep):
#     db_provider = await session.get(Provider, provider_id)
#     await session.delete(db_provider)
#     await session.commit()
#     return {"message": "Provider deleted successfully", "deleted": db_provider}


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


# @app.put("/games/{game_id}", tags=["Game"])
# async def update_game(game_id: int, data: GameCreate, session: SessionDep):
#     db_game = await session.get(Game, game_id)
#     db_game.title = data.title
#     db_game.price = data.price
#     db_game.provider_id = data.provider_id
#     await session.commit()
#     return {"succses": True, "id": game_id, "send": db_game}


# @app.delete("/games/{game_id}", tags=["Game"])
# async def delete_game(game_id: int, session: SessionDep):
#     db_game = await session.get(Game, game_id)
#     await session.delete(db_game)
#     await session.commit()
#     return {"message": "Game deleted successfully", "deleted": db_game}
