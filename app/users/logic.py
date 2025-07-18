from dataclasses import dataclass

from sqlalchemy import select

from app.users.models import UserProfile
from app.users.schemas import UserCreateSchema
from app.database import SessionDep


@dataclass
class UserLogic:
    session: SessionDep

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        query_res = await self.session.execute(query)
        user_ids = [row[0] for row in query_res]
        if user_ids:
            return await self.session.get(UserProfile, user_ids[0])

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        db_user = UserProfile(
            id=user.id,
            username=user.username,
            password=user.password,
            email=user.email,
            name=user.name
        )
        self.session.add(db_user)
        await self.session.commit()
        return await self.get_user(user.id)

    async def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        query_res = await self.session.execute(query)
        user_ids = [row[0] for row in query_res]
        if user_ids:
            return await self.session.get(UserProfile, user_ids[0])

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        query_res = await self.session.execute(query)
        user_ids = [row[0] for row in query_res]
        if user_ids:
            return await self.session.get(UserProfile, user_ids[0])
