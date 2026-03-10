from fastapi import HTTPException, status

from src.app.database.db import AsyncSession
from src.app.database.models import CryptoCurrency
from src.app.utils.external_api import CMCServiceApi
from src.app.repositories.crypto_currency_repository import BaseCryptoCurrencyRepository
from src.app.repositories.market_snapshots_repository import BaseMarketSnapshotRepository


class CryptoCurrencyService:
    def __init__(self, session: AsyncSession, cmc_api_service: CMCServiceApi):
        self.session = session
        self.cmc_api_service = cmc_api_service
        self.crypto_currency_repo = BaseCryptoCurrencyRepository(session=self.session)
        self.market_snapshot_repo = BaseMarketSnapshotRepository(session=self.session)

    async def add_crypto_currencies_in_db(self, limit: int = 5):
        crypto_listing = await self.cmc_api_service.get_crypto_listing(limit=limit)

        cmc_ids = [crypto["id"] for crypto in crypto_listing]

        existing_currencies = await self.crypto_currency_repo.find_with_cmc_ids(cmc_ids=cmc_ids)

        currency_map = {
            currency.cmc_id: currency
            for currency in existing_currencies
        }

        new_currencies = []

        for crypto in crypto_listing:
            cmc_id = crypto["id"]

            if cmc_id in currency_map:
                continue

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
        
        if new_currencies:
            self.session.add_all(new_currencies)
            await self.session.commit()

        return {"detail": f"Crypto currencies added: {len(new_currencies)}"}

    async def get_all_crypto_currencies(self, symbol: str | None = None, days: int | None = None):
        if not symbol:
            crypto_currencies = await self.crypto_currency_repo.find_all_with_relation()
            return crypto_currencies
        else:
            if not days:
                crypto_currencies = await self.crypto_currency_repo.find_with_symbol(symbol=symbol)

                if not crypto_currencies:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Crypto currency with this symbol not found."
                    )
                
                return crypto_currencies
            else:
                market_snapshots = await self.crypto_currency_repo.find_with_symbol(symbol=symbol, days=days)

                if not market_snapshots:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Crypto currency with this symbol not found."
                    )
                return market_snapshots
            
    async def get_top_gainers(self, limit: int = 10):
        top_gainers_crypto_currencies = await self.crypto_currency_repo.get_top_gainers(limit=limit)

        return top_gainers_crypto_currencies
    
    async def get_top_losers(self, limit: int = 10):
        top_losers_crypto_currencies = await self.crypto_currency_repo.get_top_losers(limit=limit)

        return top_losers_crypto_currencies
