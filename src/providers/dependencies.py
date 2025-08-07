
from .repositories import ProviderRepository
from .services import ProviderService


def provider_service():
    return ProviderService(ProviderRepository)
