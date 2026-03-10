from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.app.database.db import AsyncSession
from src.app.database.models import CryptoCurrency, MarketSnapshot
from src.app.utils.external_api import CMCServiceApi
from src.app.repositories.crypto_currency_repository import BaseCryptoCurrencyRepository
from src.app.repositories.market_snapshots_repository import BaseMarketSnapshotRepository


class MarketSyncService:
    def __init__(self, session: AsyncSession, cmc_api_service: CMCServiceApi):
        self.session = session
        self.cmc_api_service = cmc_api_service
        self.crypto_currency_repo = BaseCryptoCurrencyRepository(session=self.session)
        self.market_snapshot_repo = BaseMarketSnapshotRepository(session=self.session)

    async def sync_market_snapshots(self, limit: int = 5):
        snapshots = []

        crypto_listing = await self.cmc_api_service.get_crypto_listing(limit=limit)
        for crypto in crypto_listing:
            cmc_id = crypto["id"]

            exisnting_currency = await self.crypto_currency_repo.get_by_custom_id(custom_id=cmc_id)
            
            if not exisnting_currency:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Crypto currency with this ID: {cmc_id}"
                )
            
            quote = crypto["quote"]["USD"]

            new_snapshot = MarketSnapshot(
                price=quote["price"],
                volume_24h=quote["volume_24h"],
                percent_change_1h=quote["percent_change_1h"],
                percent_change_24h=quote["percent_change_24h"],
                market_cap=quote["market_cap"],
                market_cap_dominance=quote["market_cap_dominance"],
                fully_diluted_market_cap=quote["fully_diluted_market_cap"],
                timestamp=datetime.now(timezone.utc),
                currency_id=exisnting_currency.id
            )

            snapshots.append(new_snapshot)
        
        self.session.add_all(snapshots)
        await self.session.commit()

        return {"detail": f"Market snapshots added: {len(snapshots)}"}
        