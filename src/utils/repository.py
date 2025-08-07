
from abc import ABC
from abc import abstractmethod

from sqlalchemy import insert, select, update

from src.database import async_session_maker
from src.games.models import Game
from src.providers.models import Provider


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError

    @abstractmethod
    async def search():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
        return res.scalar_one()

    async def find_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0] for row in res.all()]
        return res

    async def find_one(self, id):
        async with async_session_maker() as session:
            data = await session.get(self.model, id)
        return data

    async def update_one(self, id, data: dict):
        async with async_session_maker() as session:
            old_data = await session.get(self.model, id)
            stmt = update(self.model).where(self.model.id).values(
                **data)
            res = await session.execute(stmt)
            await session.commit()
        return res

    async def delete_one(self, id):
        async with async_session_maker() as session:
            data = await self.find_one(id)
            await session.delete(data)
            await session.commit()
        return data


class GameSearch(SQLAlchemyRepository):

    async def search(self, query: str):
        async with async_session_maker() as session:
            stmt = select(Game.id).where(Game.title.ilike(f"%{query}%"))
            res = await session.execute(stmt)
            res = [row[0] for row in res]
        return res


class ProviderSearch(SQLAlchemyRepository):

    async def search(self, query: str):
        async with async_session_maker() as session:
            stmt = select(Provider.id).where(
                Provider.name.ilike(f"%{query}%"))
            res = await session.execute(stmt)
            res = [row[0] for row in res]
        return res
