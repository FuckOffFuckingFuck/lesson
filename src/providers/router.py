
from fastapi import APIRouter

from src.database import SessionDep

from .schemas import ProviderCreate
from .models import Provider

router = APIRouter(prefix="/providers", tags=["Provider"])
# router = FastAPI()


@router.post("/")
async def create_provider(data: ProviderCreate, session: SessionDep):
    db_provider = Provider(name=data.name, email=data.email)
    session.add(db_provider)
    await session.commit()
    return {"succses": True, "send": db_provider}


@router.get("/{provider_id}")
async def read_provider(provider_id: int, session: SessionDep):
    provider = await session.get(Provider, provider_id)
    return {"succses": True, "id": provider_id, "send": provider}


@router.put("/{provider_id}")
async def update_provider(provider_id: int, data: ProviderCreate, session: SessionDep):
    db_provider = await session.get(Provider, provider_id)
    db_provider.name = data.name
    db_provider.email = data.email
    await session.commit()
    return {"succses": True, "id": provider_id, "send": db_provider}


@router.delete("/{provider_id}")
async def delete_provider(provider_id: int, session: SessionDep):
    db_provider = await session.get(Provider, provider_id)
    await session.delete(db_provider)
    await session.commit()
    return {"message": "Provider deleted successfully", "deleted": db_provider}


# if __name__ == "__router__":
#     uvicorn.run("main:app", reload=True)
