from sqlalchemy import select, asc, desc
from sqlalchemy.orm import selectinload
import datetime

from src.app.database.db import AsyncSession
from .base_repository import Repository
from src.app.database.models import CryptoCurrency, MarketSnapshot

   
class BaseCryptoCurrencyRepository(Repository):
    model = CryptoCurrency

    async def find_with_cmc_ids(self, cmc_ids: list[int]):
        result = await self.session.execute(
            select(self.model).where(self.model.cmc_id.in_(cmc_ids))
        )
        return result.scalars().all()

    async def find_all_with_relation(self):
        result = await self.session.execute(
            select(self.model)
            .options(selectinload(self.model.snapshots))
        )
        crypto_currencies_with_snapshots = result.scalars().all()

        return crypto_currencies_with_snapshots
    
    async def find_with_symbol(self, symbol: str, days: int | None = None) -> None:
        result = await self.session.execute(
            select(self.model)
            .where(self.model.symbol == symbol)
            .options(selectinload(self.model.snapshots))
        )
        crypto_currency_with_snapshots = result.scalar_one_or_none()

        if not crypto_currency_with_snapshots:
            return None

        if not days:
            return crypto_currency_with_snapshots
        else:
            period = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days)

            result = await self.session.execute(
                select(MarketSnapshot)
                .where(
                    MarketSnapshot.currency_id == crypto_currency_with_snapshots.id,
                    MarketSnapshot.timestamp >= period
                )
                .order_by(MarketSnapshot.timestamp)
            )

        return result.scalars().all()
    
    async def get_top_gainers(self, limit: int = 10):
        result  = await self.session.execute(
            select(self.model, MarketSnapshot)
            .join(MarketSnapshot)
            .options(selectinload(self.model.snapshots))
            .order_by(asc(MarketSnapshot.percent_change_24h))
            .limit(limit)
        )

        return result.scalars().all()
    
    async def get_top_losers(self, limit: int = 10):
        result  = await self.session.execute(
            select(self.model, MarketSnapshot)
            .join(MarketSnapshot)
            .options(selectinload(self.model.snapshots))
            .order_by(desc(MarketSnapshot.percent_change_24h))
            .limit(limit)
        )

        return result.scalars().all()


