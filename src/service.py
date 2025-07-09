import json

from cache import redis_cache, RedisCache
from database import SessionDep
from models import Game
from models import Provider
from sqlalchemy import select


class SearchResult:

    def __init__(self):
        self.providers: str
        self.games: str
    
        

# # сделать поисковой обработчик
# async def search(query: str | None, session: SessionDep):

#     if query:
#         redis_query = await redis_cache.get(query)
#         if redis_query:
#             ...  # загружаем из кеша
#             return result

#         games_stmt = select(Game.id, Game.provider_id).where(
#             Game.title.ilike(f"%{query}%"))  # Иначе достаем из дб данные
#         games_result = await session.execute(games_stmt)  # хз
#         rows = games_result.all()
#         print(rows)
#         # FIX 'some_answ'
#         await redis_cache.set(query, some_answ.model_dump_json())


# @app.get("/search/", tags=["Search"])
async def search(query: str | None, session: SessionDep):
    result = SearchResult()  # хз зачем. класс поиска

    if query:  # если что-то есть в запросе
        redis_query = await redis_cache.get(query)  # достаем кеш по запросу
        if redis_query:  # если кеш есть, то ...
            # ... то загружаем из кеша json
            cached_result = json.loads(redis_query)
            cached_result['cache'] = True
            return cached_result

        games_stmt = select(Game.id, Game.provider_id).where(
            Game.title.ilike(f"%{query}%"))  # Иначе достаем из дб данные
        games_result = await session.execute(games_stmt)  # хз
        rows = games_result.all()  # достаются строки дб

        if rows:  # если строки не пустые, то ...

            game_ids = [row[0] for row in rows]
            provider_ids = [row[0]for row in rows]
            result.games = game_ids
            result.provider = provider_ids

            provider_stmt = select(Provider.id, Provider.provider_id).where(Provider.title.ilike(f"%{query}%"))
            provider_result = await session.execute(provider_stmt)
            provider_ids_from_name = [row[0] for row in provider_result]

            result.providers = list(
                set(provider_ids + provider_ids_from_name))
        await redis_cache.set(query, result.model_dump_json())
    return result


@app.get("/providers/{provider_id}", tags=["Provider"])
async def read_provider(provider_id: int, session: SessionDep):
    provider = await session.get(Provider, provider_id)
    return {"succses": True, "id": provider_id, "send": provider}


@app.get("/games/{game_id}", tags=["Game"])
async def read_game(game_id: int, session: SessionDep):
    game = await session.get(Game, game_id)
    return {"succses": True, "id": game_id, "send": game}
