from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from .base_repository import Repository
from src.app.database.models import CryptoCurrency


class AbstractCryptoCurrencyRepository(ABC):
    @abstractmethod
    async def get_cmc_by_id(self, cmc_id: int):
        raise NotImplementedError
    

class BaseCryptoCurrencyRepository(Repository):
    model = CryptoCurrency
        

class CryptoCurrencyRepository(AbstractCryptoCurrencyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cmc_by_id(self, cmc_id: int):
        result = await self.session.execute(
            select(CryptoCurrency).where(CryptoCurrency.cmc_id == cmc_id)
        )
        existing_crypto_currency = result.scalar_one_or_none()

        return existing_crypto_currency


    


