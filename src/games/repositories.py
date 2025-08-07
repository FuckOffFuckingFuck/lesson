
from src.utils.repository import GameSearch

from .models import Game


class GameRepository(GameSearch):
    model = Game
