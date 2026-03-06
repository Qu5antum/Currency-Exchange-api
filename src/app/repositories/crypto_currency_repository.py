from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from .base_repository import Repository
from src.app.database.models import CryptoCurrency

    
class BaseCryptoCurrencyRepository(Repository):
    model = CryptoCurrency
        


    


