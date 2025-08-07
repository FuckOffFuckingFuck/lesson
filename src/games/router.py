from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from .schemas import GameCreate
from .services import GameService
from .dependencies import game_service


router = APIRouter(prefix="/games", tags=["Game"])


@router.post("/")
async def create_game(
    game_data: GameCreate,
    game_service: Annotated[GameService, Depends(game_service)]
):
    game_id = await game_service.create_game(game_data)
    return {"succses": True, "game_id": game_id}


@router.get("/{game_id}")
async def read_game(
    game_id: int,
    game_service: Annotated[GameService, Depends(game_service)]
):
    game_data = await game_service.read_game(game_id)
    return {"succses": True, "game_data": game_data}


@router.put("/{game_id}")
async def update_game(
    game_id: int,
    game_data: GameCreate,
    game_service: Annotated[GameService, Depends(game_service)]
):
    await game_service.update_game(game_id, game_data)
    return {"succses": True, "game_id": game_id, "game_data": game_data}


@router.delete("/{game_id}")
async def delete_game(
    game_id: int,
    game_service: Annotated[GameService, Depends(game_service)]
):
    game_data = await game_service.delete_game(game_id)
    return {"succses": True, "deleted": game_data}
