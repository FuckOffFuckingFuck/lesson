
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy.orm import relationship

from src.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    price = Column(Numeric(10, 2))
    is_published = Column(Boolean, default=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))

    provider = relationship("Provider", back_populates="games")
