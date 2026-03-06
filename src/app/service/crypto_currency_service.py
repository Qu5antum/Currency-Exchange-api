from fastapi import HTTPException, status, Depends
import datetime

from src.app.database.db import AsyncSession
from src.app.api.dependencies.dependency import get_http_client
from src.app.utils.external_api import CMCServiceApi
from src.app.repositories.crypto_currency_repository import BaseCryptoCurrencyRepository
from src.app.repositories.market_snapshots_repository import BaseMarketSnapshotRepository
from src.app.api.schemas.crypto_currency import CryptoCurrencyCreate, MarketSnapshotCreate


class MarketSyncService:
    def __init__(self, session: AsyncSession, cmc_api_service: CMCServiceApi = Depends(get_http_client)):
        self.session = session
        self.cmc_api_service = cmc_api_service
        self.crypto_currency_repo = BaseCryptoCurrencyRepository(session=self.session)
        self.market_snapshot_repo = BaseMarketSnapshotRepository(session=self.session)

    async def sync_crypto_currencies(self, limit: int = 5):
        crypto_listing = await self.cmc_api_service.get_crypto_listing(limit=limit)


        for crypto in crypto_listing:
            existing_crypto_currency = await self.crypto_currency_repo.get_by_custom_id(custom_id=crypto_currency["id"])

            if not existing_crypto_currency:
                new_crypto = CryptoCurrencyCreate(
                    cmc_id=crypto["id"],
                    name=crypto["name"],
                    symbol=crypto["symbol"],
                    max_supply=crypto["max_supply"],
                    circulating_supply=crypto["circulating_supply"],
                    total_supply=crypto["total_supply"],
                    cmc_rank=crypto["cmc_rank"]
                )

                crypto_currency = await self.crypto_currency_repo.create(new_crypto.model_dump())
            else:
                crypto_currency = existing_crypto_currency

            quote = crypto["quote"]["USD"]

            snapshot_schema = MarketSnapshotCreate(
                price=quote["price"],
                volume_24h=quote["volume_24"],
                percent_change_1h=quote["percent_change_1h"],
                percent_change_24h=quote["percent_change_24h"],
                market_cap=quote["market_cap"],
                market_cap_dominance=quote["market_cap_dominance"],
                fully_diluted_market_cap=quote["fully_diluted_market_cap"],
                currency_id=crypto_currency.id
            )

            await self.market_snapshot_repo.create(snapshot_schema.model_dump())

        await self.session.commit()
    


                

        




            


            
            





