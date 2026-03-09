from sqlalchemy import select
from sqlalchemy.orm import selectinload
import datetime

from src.app.database.db import AsyncSession
from .base_repository import Repository
from src.app.database.models import CryptoCurrency, MarketSnapshot

   
class BaseCryptoCurrencyRepository(Repository):
    model = CryptoCurrency

    async def find_all_with_relation(self):
        result = await self.session.execute(
            select(CryptoCurrency)
            .options(selectinload(CryptoCurrency.snapshots))
        )
        crypto_currencies_with_snapshots = result.scalars().all()

        return crypto_currencies_with_snapshots
    
    async def find_with_symbol(self, symbol: str, days: int | None = None) -> None:
        result = await self.session.execute(
            select(CryptoCurrency)
            .where(CryptoCurrency.symbol == symbol)
            .options(selectinload(CryptoCurrency.snapshots))
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
    


