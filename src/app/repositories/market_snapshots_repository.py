from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from .base_repository import Repository
from src.app.database.models import MarketSnapshot


class BaseMarketSnapshotRepository(Repository):
    model = MarketSnapshot

    async def get_latest_snapshot(self, crypto_currency_id: int):
        result = await self.session.execute(
            select(MarketSnapshot.price)
            .where(MarketSnapshot.currency_id == crypto_currency_id)
            .order_by(MarketSnapshot.timestamp.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()




    

        