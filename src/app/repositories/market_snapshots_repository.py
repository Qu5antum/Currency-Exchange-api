from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from .base_repository import Repository
from src.app.database.models import MarketSnapshot


class BaseMarketSnapshotRepository(Repository):
    model = MarketSnapshot




    

        