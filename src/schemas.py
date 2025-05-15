from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import ConfigDict


class ProviderCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Gabe",
                "email": "GabeLoganNewell@gmail.com"
            }
        }
    )

    name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=255)


class GameCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Cyberpunk 2077",
                "price": 59.99,
                "provider_id": 1
            }
        }
    )

    title: str = Field(max_length=200)
    price: float = Field(ge=0)
    # provider_id: int
