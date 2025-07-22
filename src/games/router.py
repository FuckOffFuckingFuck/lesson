
from fastapi import APIRouter

from src.database import SessionDep

from .models import Game
from .schemas import GameCreate


router = APIRouter(prefix="/games", tags=["Game"])


@router.post("/")
async def create_game(data: GameCreate, session: SessionDep):
    db_game = Game(
        title=data.title,
        price=data.price,
        provider_id=data.provider_id
    )
    session.add(db_game)
    await session.commit()
    return {"succses": True, "send": db_game}


@router.get("/{game_id}")
async def read_game(game_id: int, session: SessionDep):
    game = await session.get(Game, game_id)
    return {"succses": True, "id": game_id, "send": game}


@router.put("/{game_id}")
async def update_game(game_id: int, data: GameCreate, session: SessionDep):
    db_game = await session.get(Game, game_id)
    db_game.title = data.title
    db_game.price = data.price
    db_game.provider_id = data.provider_id
    await session.commit()
    return {"succses": True, "id": game_id, "send": db_game}


@router.delete("/{game_id}")
async def delete_game(game_id: int, session: SessionDep):
    db_game = await session.get(Game, game_id)
    await session.delete(db_game)
    await session.commit()
    return {"message": "Game deleted successfully", "deleted": db_game}
