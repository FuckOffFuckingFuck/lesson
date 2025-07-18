from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.users.auth.service import AuthService
from app.exceptions import UserNotFoundException
from app.exceptions import UserNotCorrectPasswordException
from app.dependency import get_auth_service
from app.users.schemas import UserLoginSchema
from app.users.schemas import UserCreateSchema


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        data = await auth_service.login(body.username, body.password)
        return data
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
