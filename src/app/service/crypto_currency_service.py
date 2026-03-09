from fastapi import HTTPException, status

from src.app.database.db import AsyncSession
from src.app.repositories.crypto_currency_repository import BaseCryptoCurrencyRepository


class CryptoCurrencyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.crypto_currency_repo = BaseCryptoCurrencyRepository(session=self.session)

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