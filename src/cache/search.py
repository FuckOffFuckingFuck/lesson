
import json

from sqlalchemy import select

from src.database import SessionDep

from src.games.models import Game
from src.providers.models import Provider
from src.games.schemas import GameCreate
from src.providers.schemas import ProviderCreate


class SearchTool():

    def __init__(self):
        self._game = None
        self._provider = None
        self._game_result = []
        self._provide_result = []

    async def search(self, query, session: SessionDep):
        if query:
            games_stmt = select(Game.id).where(  # , Game.provider_id
                Game.title.ilike(f"%{query}%"))
            games_result = await session.execute(games_stmt)
            self._game = [row[0] for row in games_result]

            provider_stmt = select(Provider.id).where(
                Provider.name.ilike(f"%{query}%"))
            provider_result = await session.execute(provider_stmt)
            self._provider = [row[0] for row in provider_result]
        return None

    async def get_all_game(self, session: SessionDep) -> list:
        if self._game:
            for game in self._game:
                db_data = await session.get(Game, game)
                game_json = dict(GameCreate(
                    title=db_data.title,
                    price=db_data.price,
                    provider_id=db_data.provider_id
                ))
                json_res = json.dumps(game_json)
                self._game_result.append(json_res)
            return self._game_result
        return None

    async def get_all_provider(self, session: SessionDep) -> list:
        if self._provider:
            for provider in self._provider:
                db_data = await session.get(Provider, provider)
                provider_json = dict(ProviderCreate(
                    name=db_data.name,
                    email=db_data.email
                ))
                json_res = json.dumps(provider_json)
                self._provide_result.append(json_res)
            return self._provide_result
        return None

    async def get_first_game(self, session: SessionDep):
        if self._game:
            db_data = await session.get(Game, self._game[0])
            game_json = dict(GameCreate(
                title=db_data.title,
                price=db_data.price,
                provider_id=db_data.provider_id
            ))
            json_res = json.dumps(game_json)
            return json_res
        return None

    async def get_first_provider(self, session: SessionDep):
        if self._provider:
            db_data = await session.get(Provider, self._provider[0])
            provider_json = dict(ProviderCreate(
                name=db_data.name,
                email=db_data.email
            ))
            json_res = json.dumps(provider_json)
            return json_res
        return None


search_client = SearchTool()  # FIX: добавить везде экземпляры класса
