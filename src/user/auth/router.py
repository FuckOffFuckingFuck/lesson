
# поправить логин


from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from fastapi import HTTPException
from fastapi import Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from authx import AuthX
from authx import AuthXConfig

from src.database import SessionDep
from src.config import settings

from ..schemas import UserSchema
from ..models import UserModel
from ..hash_pass import HashPassword
from ..service import search_username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth_actions/login")

config = AuthXConfig(
    JWT_SECRET_KEY=settings.SECRET_KEY,
    JWT_ALGORITHM=settings.ALGORITHM,
    JWT_ACCESS_COOKIE_NAME=settings.ACCESS_COOKIE_NAME,
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_CSRF_PROTECT=False  # FIX ???
)

auth = AuthX(config=config)

router = APIRouter(prefix="/auth_actions", tags=["Auth actions"])


@router.post("/login")
async def login(
    creds: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    response: Response
):
    user_id = await search_username(creds.username, session)
    user_dict = await session.get(UserModel, user_id)
    if not user_dict:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not HashPassword.verify(user_dict.hashed_password, creds.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = auth.create_access_token(uid=user_dict.username)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(token: UserSchema = Depends(oauth2_scheme)):
    try:
        return token
    except Exception as e:
        raise HTTPException(401, detail={"msg": str(e)}) from e


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"msg": "You have successfully logged out of your account"}
