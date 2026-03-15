from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.app.database.db import AsyncSession
from src.app.database.models import Portfolio, PortfolioAsset, PortfolioTransaction, User
from src.app.repositories.portfolio_repository import PortfolioRepostory
from src.app.repositories.crypto_currency_repository import BaseCryptoCurrencyRepository
from src.app.api.schemas.crypto_currency import BuyCryptoRequest


class PortfolioService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.portfolio_repo = PortfolioRepostory(session=self.session)
        self.crypto_repo = BaseCryptoCurrencyRepository(session=self.session)

    async def add_portfolio_for_user(self, name: str, user: User):
        new_portfolio = Portfolio(
            name=name,
            user_id=user.id
        )

        await self.portfolio_repo.create(data=new_portfolio)
        await self.session.commit()
        await self.session.refresh(new_portfolio)

        return {
            "message": "New Portfolio created.",
            "detail": new_portfolio
        }
    
    async def buy_crypto(self, portfolio_id: int, data: BuyCryptoRequest):
        crypto_currency = await self.crypto_repo.get_by_symbol(symbol=data.symbol)
        
        if not crypto_currency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crypto Currency not found."
            )
        
        asset = await self.portfolio_repo.get_asset(portfolio_id=portfolio_id)

        if asset:
            new_amout = asset.amount + data.amount

            asset.avg_buy_price = (asset.amount * asset.avg_buy_price + data.amount * data.price) / new_amout

            asset.amount = new_amout
        else:
            asset = PortfolioAsset(
                portfolio_id=portfolio_id,
                crypto_currency_id=crypto_currency.id,
                amount=data.amount,
                symbol=data.symbol
            )
            self.session.add(asset)

        transaction = PortfolioTransaction(
            type="BUY",
            amount=data.amount,
            price=data.price,
            timestamp=datetime.now(timezone.utc),
            portfolio_id=portfolio_id,
            crypto_currency_id=crypto_currency.id
        )
        self.session.add(transaction)

        await self.session.commit()

        return {
            "message": "Crypto purchased",
            "asset": asset
        }
        
        
            
            

    



