from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    hashed_password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserAuthSchema(BaseModel):
    pass
