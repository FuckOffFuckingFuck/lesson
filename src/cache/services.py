
from src.utils.repository import AbstractRepository


class GameSearchService:

    def __init__(self, game_repo: AbstractRepository):
        self.game_repo: AbstractRepository = game_repo()

    async def search(self, query):
        game_id = await self.game_repo.search(query)
        game_data = [await self.game_repo.find_one(row) for row in game_id]
        return game_data


class ProviderSearchService:

    def __init__(self, provider_repo: AbstractRepository):
        self.provider_repo: AbstractRepository = provider_repo()

    async def search(self, query):
        provider_id = await self.provider_repo.search(query)
        provider_data = [await self.provider_repo.find_one(row) for row in provider_id]
        return provider_data
