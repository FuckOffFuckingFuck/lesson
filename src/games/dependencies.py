
from .repositories import GameRepository
from .services import GameService


def game_service():
    return GameService(GameRepository)
