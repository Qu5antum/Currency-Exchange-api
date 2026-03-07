from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.app.database.db import AsyncSession
from src.app.database.models import CryptoCurrency, MarketSnapshot
from src.app.database.models import CryptoCurrency
from src.app.utils.external_api import CMCServiceApi
from src.app.repositories.crypto_currency_repository import BaseCryptoCurrencyRepository
from src.app.repositories.market_snapshots_repository import BaseMarketSnapshotRepository


class MarketSyncService:
    def __init__(self, session: AsyncSession, cmc_api_service: CMCServiceApi):
        self.session = session
        self.cmc_api_service = cmc_api_service
        self.crypto_currency_repo = BaseCryptoCurrencyRepository(session=self.session)
        self.market_snapshot_repo = BaseMarketSnapshotRepository(session=self.session)

    async def sync_crypto_currencies(self, limit: int = 5):
        crypto_listing = await self.cmc_api_service.get_crypto_listing(limit=limit)

        cmc_ids = [crypto["id"] for crypto in crypto_listing]

        existing_currencies = await self.crypto_currency_repo.find_all_with_custom_ids(obj_ids=cmc_ids)

        currency_map = {
            currency.cmc_id: currency
            for currency in existing_currencies
        }

        new_currencies = []
        snapshots = []

        for crypto in crypto_listing:
            cmc_id = crypto["id"]
            currency = currency_map.get(cmc_id)

            if not currency:
                new_crypto = CryptoCurrency(
                    cmc_id=crypto["id"],
                    name=crypto["name"],
                    symbol=crypto["symbol"],
                    max_supply=crypto["max_supply"],
                    circulating_supply=crypto["circulating_supply"],
                    total_supply=crypto["total_supply"],
                    cmc_rank=crypto["cmc_rank"]
                )

                new_currencies.append(new_crypto)
                currency_map[cmc_id] = new_crypto

        if new_currencies:
            self.session.add_all(new_currencies)
            await self.session.flush()

            for crypto in crypto_listing:
                cmc_id = crypto["id"]
                currency = currency_map[cmc_id]
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
                    currency_id=currency.id
                )

                snapshots.append(new_snapshot)

        self.session.add_all(snapshots)

        await self.session.commit()

        return {
            "currencies_added": len(new_currencies),
            "snapshots_created": len(snapshots)
        }
    


                

        




            


            
            





