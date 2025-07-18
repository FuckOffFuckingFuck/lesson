from typing import Annotated
from fastapi import Depends

from app.users.auth.service import AuthService
from app.users.logic import UserLogic
from app.users.service import UserService

from app.database import SessionDep


async def get_user_logic(session: SessionDep) -> UserLogic:
    return UserLogic(session=session)


async def get_auth_service(user_logic: Annotated[UserLogic, Depends(get_user_logic)]) -> AuthService:
    return AuthService(user_logic)


async def get_user_service(
    user_logic: Annotated[UserLogic, Depends(get_user_logic)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserService:
    return UserService(
        user_logic=user_logic, auth_service=auth_service
    )
