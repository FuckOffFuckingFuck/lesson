from sqlalchemy.exc import IntegrityError

from src.utils.repository import AbstractRepository

from .schemas import ProviderCreate


class ProviderService:

    def __init__(self, provider_repo: AbstractRepository):
        self.provider_repo: AbstractRepository = provider_repo()

    async def create_provider(self, provider_data: ProviderCreate):
        try:
            provider_dict = provider_data.model_dump()
            provider_id = await self.provider_repo.add_one(provider_dict)
            return provider_id
        except IntegrityError:
            return f"Provider already created"

    async def read_provider(self, provider_id):
        provider_data = await self.provider_repo.find_one(provider_id)
        return provider_data

    async def update_provider(self, provider_id, provider_data: ProviderCreate):
        try:
            provider_dict = provider_data.model_dump()
            provider_id = await self.provider_repo.update_one(provider_id, provider_dict)
            return provider_id
        except IntegrityError:
            return f"Use unique name"

    async def delete_provider(self, provider_id):
        try:
            provider_data = await self.provider_repo.delete_one(provider_id)
            return provider_data
        except:
            return f"Provider already deleted"

    async def find_all(self):
        data = await self.provider_repo.find_all()
        return data
