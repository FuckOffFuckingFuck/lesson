from sqlalchemy.exc import IntegrityError

from src.utils.repository import AbstractRepository

from .schemas import GameCreate


class GameService:

    def __init__(self, game_repo: AbstractRepository):
        self.game_repo: AbstractRepository = game_repo()

    async def create_game(self, game_data: GameCreate):
        try:
            game_dict = game_data.model_dump()
            game_id = await self.game_repo.add_one(game_dict)
            return game_id
        except IntegrityError:
            return f"Game already created"

    async def read_game(self, game_id):
        game_data = await self.game_repo.find_one(game_id)
        return game_data

    async def update_game(self, game_id, game_data: GameCreate):
        game_dict = game_data.model_dump()
        game_id = await self.game_repo.update_one(game_id, game_dict)
        return game_id

    async def delete_game(self, game_id):
        try:
            game_data = await self.game_repo.delete_one(game_id)
            return game_data
        except:
            return f"Game already deleted"

    async def find_all(self):
        data = await self.game_repo.find_all()
        return data
