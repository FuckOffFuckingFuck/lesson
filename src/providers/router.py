from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends

from .schemas import ProviderCreate
from .services import ProviderService
from .dependencies import provider_service


router = APIRouter(prefix="/providers", tags=["Provider"])


@router.post("/")
async def create_provider(
    provider_data: ProviderCreate,
    provider_service: Annotated[ProviderService, Depends(provider_service)]
):
    provider_id = await provider_service.create_provider(provider_data)
    return {"succses": True, "provider_id": provider_id}


@router.get("/{provider_id}")
async def read_provider(
    provider_id: int,
    provider_service: Annotated[ProviderService, Depends(provider_service)]
):
    provider_data = await provider_service.read_provider(provider_id)
    return {"succses": True, "provider_data": provider_data}


@router.put("/{provider_id}")
async def update_provider(
    provider_id: int,
    provider_data: ProviderCreate,
    provider_service: Annotated[ProviderService, Depends(provider_service)]
):
    await provider_service.update_provider(provider_id, provider_data)
    return {"succses": True, "provider_id": provider_id, "provider_data": provider_data}


@router.delete("/{provider_id}")
async def delete_provider(
    provider_id: int,
    provider_service: Annotated[ProviderService, Depends(provider_service)]
):
    provider_data = await provider_service.delete_provider(provider_id)
    return {"succses": True, "deleted": provider_data}
