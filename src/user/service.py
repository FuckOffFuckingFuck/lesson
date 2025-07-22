from sqlalchemy import select

from src.database import SessionDep
from .models import UserModel
# from schemas import UserSchema


async def search_username(query: str, session: SessionDep) -> int | None:
    if query:
        users_stmt = select(UserModel.id).where(
            UserModel.username.like(query))
        users_result = await session.execute(users_stmt)
        user = [row[0] for row in users_result]
        if user:
            return user[0]
    return None


async def return_username_data(user_id: int | None, session: SessionDep):
    if user_id:
        user = await session.get(UserModel, user_id)
        return user
    return None


# async def get_user(session: SessionDep, id: int = None, username: str = None, email: str = None):
#     if id:
#         res_stmt = select(UserModel).filter(UserModel.id == id)
#     if username:
#         res_stmt = select(UserModel).filter(UserModel.username == username)
#     if email:
#         res_stmt = select(UserModel).filter(UserModel.email == email)
#     res = await session.execute(res_stmt)
#     return UserSchema(res)
