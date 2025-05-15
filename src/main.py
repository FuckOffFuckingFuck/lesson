
import uvicorn
from fastapi import FastAPI

from models import Game
from models import Provider
from database import SessionDep
from schemas import GameCreate
from schemas import ProviderCreate
from sqlalchemy import select


app = FastAPI()


@app.post("/providers/", tags=["Provider"])
async def create_provider(data: ProviderCreate, session: SessionDep):
    db_provider = Provider(name=data.name, email=data.email)
    session.add(db_provider)
    await session.commit()
    return {"succses": True, "send": db_provider}


@app.get("/providers/{provider_id}", tags=["Provider"])
async def read_provider(provider_id: int, session: SessionDep):
    provider = await session.get(Provider, provider_id)
    return {"succses": True, "id": provider_id, "send": provider}


@app.put("/providers/{provider_id}", tags=["Provider"])
async def update_provider(provider_id: int, data: ProviderCreate, session: SessionDep):
    db_provider = await session.get(Provider, provider_id)
    db_provider.name = data.name
    db_provider.email = data.email
    await session.commit()
    return {"succses": True, "id": provider_id, "send": db_provider}


@app.delete("/providers/{provider_id}", tags=["Provider"])
async def delete_provider(provider_id: int, session: SessionDep):
    db_provider = await session.get(Provider, provider_id)
    await session.delete(db_provider)
    await session.commit()
    return {"message": "Provider deleted successfully", "deleted": db_provider}


@app.post("/games/", tags=["Game"])
async def create_game(data: GameCreate, session: SessionDep):
    db_game = Game(
        title=data.title,
        price=data.price,
        provider_id=data.provider_id
    )
    session.add(db_game)
    await session.commit()
    return {"succses": True, "send": db_game}


@app.get("/games/{game_id}", tags=["Game"])
async def read_game(game_id: int, session: SessionDep):
    game = await session.get(Game, game_id)
    return {"succses": True, "id": game_id, "send": game}


@app.put("/games/{game_id}", tags=["Game"])
async def update_game(game_id: int, data: GameCreate, session: SessionDep):
    db_game = await session.get(Game, game_id)
    db_game.title = data.title
    db_game.price = data.price
    db_game.provider_id = data.provider_id
    await session.commit()
    return {"succses": True, "id": game_id, "send": db_game}


@app.delete("/games/{game_id}", tags=["Game"])
async def delete_game(game_id: int, session: SessionDep):
    db_game = await session.get(Game, game_id)
    await session.delete(db_game)
    await session.commit()
    return {"message": "Game deleted successfully", "deleted": db_game}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
