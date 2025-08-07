
from src.utils.repository import ProviderSearch

from .models import Provider


class ProviderRepository(ProviderSearch):
    model = Provider
