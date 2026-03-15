from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.app.database.db import AsyncSession
from src.app.database.models import Portfolio, PortfolioAsset, PortfolioTransaction, User
from src.app.repositories.portfolio_repository import PortfolioRepostory
from src.app.repositories.crypto_currency_repository import BaseCryptoCurrencyRepository
from src.app.repositories.market_snapshots_repository import BaseMarketSnapshotRepository
from src.app.api.schemas.crypto_currency import BuyCryptoRequest, SellCryptoRequest


class PortfolioService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.portfolio_repo = PortfolioRepostory(session=self.session)
        self.crypto_repo = BaseCryptoCurrencyRepository(session=self.session)
        self.market_repo = BaseMarketSnapshotRepository(session=self.session)

    async def add_portfolio_for_user(self, name: str, user: User):
        new_portfolio = Portfolio(
            name=name,
            user_id=user.id
        )

        await self.portfolio_repo.create(model=new_portfolio)
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
        
        asset = await self.portfolio_repo.get_asset(portfolio_id=portfolio_id, crypto_currency_id=crypto_currency.id)

        if asset:
            new_amount = asset.amount + data.amount

            asset.avg_buy_price = (asset.amount * asset.avg_buy_price + data.amount * data.price) / new_amount

            asset.amount = new_amount
        else:
            asset = PortfolioAsset(
                portfolio_id=portfolio_id,
                crypto_currency_id=crypto_currency.id,
                amount=data.amount,
                avg_buy_price=data.price
            )
            self.session.add(asset)

        transaction = PortfolioTransaction(
            type="BUY",
            amount=data.amount,
            price=data.price,
            portfolio_id=portfolio_id,
            crypto_currency_id=crypto_currency.id
        )
        self.session.add(transaction)

        await self.session.commit()
        await self.session.refresh(asset)

        return {
            "message": "Crypto purchased",
            "asset": asset
        }
    
    async def sell_crypto(self, portfolio_id, data: SellCryptoRequest):
        crypto_currency = await self.crypto_repo.get_by_symbol(symbol=data.symbol)

        if not crypto_currency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crypto currency not found."
            )
        
        asset = await self.portfolio_repo.get_asset(portfolio_id=portfolio_id, crypto_currency_id=crypto_currency.id)

        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found in portfolio"
            )
        
        if asset.amount < data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough crypto to sell"
            )
        
        asset.amount -= data.amount

        if asset.amount == 0:
            await self.session.delete(asset)

        transaction = PortfolioTransaction(
            type="SELL",
            amount=data.amount,
            price=data.price,
            portfolio_id=portfolio_id,
            crypto_currency_id=crypto_currency.id
        )

        self.session.add(transaction)

        await self.session.commit()

        return {
            "message": "Crypto sold."
        }
        
            
            

    



