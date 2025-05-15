from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy.orm import relationship

from database import Base
from database import async_engine
import asyncio


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    email = Column(String(255))

    games = relationship("Game", back_populates="provider")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    price = Column(Numeric(10, 2))
    is_published = Column(Boolean, default=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))

    provider = relationship("Provider", back_populates="games")


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(init_db())
