
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.database import Base
from .schemas import ProviderSchema


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    email = Column(String(255))

    games = relationship("Game", back_populates="provider")

    def to_read_model(self) -> ProviderSchema:
        return ProviderSchema(
            id=self.id,
            name=self.name,
            email=self.email
        )
