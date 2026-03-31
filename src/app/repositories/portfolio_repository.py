from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime

from src.app.database.models import Portfolio, PortfolioAsset, PortfolioTransaction, CryptoCurrency
from .base_repository import Repository
from src.app.api.schemas.portfolio import TransactionRequest, TransactionType


class PortfolioRepostory(Repository):
    model = Portfolio

    async def get_asset(self, portfolio_id: int, crypto_currency_id: int):
        result = await self.session.execute(
            select(PortfolioAsset)
            .where(
                PortfolioAsset.portfolio_id == portfolio_id,
                PortfolioAsset.crypto_currency_id == crypto_currency_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_asset_by_portfolio_id(self, portfolio_id: int):
        result = await self.session.execute(
            select(PortfolioAsset)
            .where(PortfolioAsset.portfolio_id == portfolio_id)
            .options(selectinload(PortfolioAsset.crypto_currency))
        )

        return result.scalars().all()
    
    async def get_user_portfolio(self, user_id: uuid.UUID, portfolio_id: int):
        result = await self.session.execute(
            select(Portfolio)
            .where(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_portfolios(self, user_id: uuid.UUID):
        result = await self.session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(selectinload(self.model.assets))
        )

        return result.scalars().all()
    
    async def get_transactions(
            self, 
            portfolio_id: int, 
            data: TransactionRequest, 
            transaction_type: TransactionType | None = None
    ):
        query = (
            select(PortfolioTransaction, CryptoCurrency.symbol)
            .join(CryptoCurrency, PortfolioTransaction.crypto_currency_id == CryptoCurrency.id)
            .where(PortfolioTransaction.portfolio_id == portfolio_id)
        )

        if transaction_type:
            query = query.where(PortfolioTransaction.type == transaction_type)
        if data.symbol:
            query = query.where(CryptoCurrency.symbol == data.symbol)
        if data.date_from:
            query = query.where(PortfolioTransaction.timestamp >= data.date_from)
        if data.date_to:
            query = query.where(PortfolioTransaction.timestamp <= data.date_to)
        
        query = (
            query.order_by(PortfolioTransaction.timestamp.desc())
            .limit(50)
        )

        result = await self.session.execute(query)

        return result.scalars().all()
    




