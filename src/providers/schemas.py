
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
