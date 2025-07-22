
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from src.declarative_base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String)
    email = Column(String(255))  # , unique=True, default=None
    full_name = Column(String(100), default=None)
    disabled = Column(Boolean, default=False)
