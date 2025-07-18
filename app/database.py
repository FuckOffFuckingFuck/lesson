# предназначено для локального тестирования приложения
# без докер образа и PostgreSQL
# используется в main.py, search.py
# .\.venv\Scripts\activate
# pip install aiosqlite

from typing import Annotated
import asyncio

from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

async_engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(init_db())
