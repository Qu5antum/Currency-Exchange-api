from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from src.app.database.models import Currency

class AbstractCurrencyRepository(ABC):
    @abstractmethod
    async def create(self, )