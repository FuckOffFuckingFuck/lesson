

from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Request, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authx import AuthX, AuthXConfig, RequestToken
from authx.exceptions import MissingTokenError
from sqlalchemy.exc import IntegrityError, OperationalError

from src.database import SessionDep

from .schemas import UserSchema
from .models import UserModel
from .hash_pass import HashPassword
from .service import search_username
from .auth.router import auth


router = APIRouter(prefix="/account_actions", tags=["Account actions"])


# @router.get("/protected", dependencies=[Depends(auth.access_token_required)])
# async def protected():
#     try:
#         pass
#         # auth.verify_token(token=token)
#         # some code
#     except Exception as e:
#         raise HTTPException(401, detail={"message": str(e)}) from e


# CRUD
@router.post("/")
async def create_user(creds: Annotated[UserSchema, Depends()], session: SessionDep):
    try:
        db_user = UserModel(
            username=creds.username,
            full_name=creds.full_name,
            email=creds.email,
            hashed_password=HashPassword.bcrypt(creds.hashed_password),
            disabled=creds.disabled
        )
        session.add(db_user)
        await session.commit()
        return {"succses": True, "msg": db_user}

    except IntegrityError:
        return {"success": False, "msg": "This username is occupied. Enter another"}
    except OperationalError as e:
        return {"success": False, "msg": e}
    except Exception as e:
        return {"success": False, "msg": e}


@router.get("/{username}", dependencies=[Depends(auth.access_token_required)])
async def get_user_data(username: str, session: SessionDep):
    try:
        user_id = await search_username(username, session)
        if user_id:
            user_db = await session.get(UserModel, user_id)
            return {"succses": True, "msg": user_db}
        return {"success": False, "msg": "Username not found"}

    except MissingTokenError as e:
        return {"success": False, "msg": e}
    except Exception as e:
        return {"success": False, "msg": e}


@router.put("/{username}", dependencies=[Depends(auth.access_token_required)])
async def update_user_data(request: Request, username: str, creds: UserSchema, session: SessionDep):
    try:
        user_id = await search_username(username, session)
        print(user_id)
        if user_id:
            user_db = await session.get(UserModel, user_id)
            print(user_db.username, creds.username)
            user_db.username = creds.username
            user_db.full_name = creds.full_name
            user_db.email = creds.email
            user_db.hashed_password = HashPassword.bcrypt(
                creds.hashed_password)
            user_db.disabled = creds.disabled
            await session.commit()
            return {"succses": True, "msg": user_db}
        return {"success": False, "msg": "Username not found"}

    except MissingTokenError as e:
        return {"success": False, "msg": e}
    except Exception as e:
        return {"success": False, "msg": e}


@router.delete("/{username}", dependencies=[Depends(auth.access_token_required)])
async def delete_username(username: str, session: SessionDep):
    try:
        user_id = await search_username(username, session)
        if user_id:
            user = await session.get(UserModel, user_id)
            await session.delete(user)
            await session.commit()
            return {"success": True, "msg": user}
        return {"success": False, "msg": "Username not found"}

    except MissingTokenError as e:
        return {"success": False, "msg": e}
    except Exception as e:
        return {"success": False, "msg": e}
