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
    
    async def buy_crypto(self, portfolio_id: int, data: BuyCryptoRequest, user: User):
        user_portfolio = await self.portfolio_repo.get_user_portfolio(user_id=user.id, portfolio_id=portfolio_id)

        if not user_portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Porfolio not found."
            )

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
    
    async def sell_crypto(self, portfolio_id: int, data: SellCryptoRequest, user: User):
        user_portfolio = await self.portfolio_repo.get_user_portfolio(user_id=user.id, portfolio_id=portfolio_id)

        if not user_portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Porfolio not found."
            )
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
    
    async def portfolio_overview(self, portfolio_id: int, user: User):
        user_portfolio = await self.portfolio_repo.get_user_portfolio(user_id=user.id, portfolio_id=portfolio_id)

        if not user_portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Porfolio not found."
            )
        
        assets = await self.portfolio_repo.get_asset_by_portfolio_id(portfolio_id=portfolio_id)

        result_assets = []

        total_value = 0
        total_profit = 0

        currency_ids = [asset.crypto_currency_id for asset in assets]
        snapshots = await self.market_repo.get_latest_snapshots(currency_ids=currency_ids)

        for asset in assets:
            snapshot = snapshots.get(asset.crypto_currency_id)
            
            if not snapshot:
                continue

            current_price = snapshot.price

            value = asset.amount * current_price
            profit = (current_price - asset.avg_buy_price) * asset.amount

            total_value += value
            total_profit += profit

            result_assets.append({
                "symbol": asset.crypto_currency.symbol,
                "amount": asset.amount,
                "avg_buy_price": asset.avg_buy_price,
                "current_price": current_price,
                "value": value,
                "profit": profit
            })

        return {
            "total_value": total_value,
            "total_profit": total_profit,
            "assets": result_assets
        }
    
    async def portfolio_distribution(self, portfolio_id: int, user: User):
        user_portfolio = await self.portfolio_repo.get_user_portfolio(user_id=user.id, portfolio_id=portfolio_id)

        if not user_portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Porfolio not found."
            )
        
        assets = await self.portfolio_repo.get_asset_by_portfolio_id(portfolio_id=portfolio_id)

        crypto_currency_ids = [asset.crypto_currency_id for asset in assets]
        snapshots = await self.market_repo.get_latest_snapshots(currency_ids=crypto_currency_ids)

        values = []
        for asset in assets:
            snapshot = snapshots.get(asset.crypto_currency_id)
            if not snapshot:
                continue

            value = asset.amount * snapshot.price
            values.append((asset, value))

        total_value = sum(v for _, v in values)
        if total_value == 0:
            return []
        
        distribution = []
        for asset, value in values:
            percent = round(value / total_value * 100, 2)
            distribution.append({
                "symbol": asset.crypto_currency.symbol,
                "distribution": percent
            })
        return distribution





            
            

    



