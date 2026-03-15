from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from .base_repository import Repository
from src.app.database.models import MarketSnapshot


class BaseMarketSnapshotRepository(Repository):
    model = MarketSnapshot

    async def get_latest_snapshots(self, currency_ids: list[int]):
        stmt = (
            select(MarketSnapshot)
            .where(MarketSnapshot.currency_id.in_(currency_ids))
            .distinct(MarketSnapshot.currency_id)
            .order_by(MarketSnapshot.currency_id, MarketSnapshot.timestamp.desc())
        )
        result = await self.session.execute(stmt)
        snapshots = {s.currency_id: s for s in result.scalars().all()}
        return snapshots




    

        