from sqlalchemy import select

from src.app.database.models import Portfolio, PortfolioAsset, PortfolioTransaction
from .base_repository import Repository


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


class PortfolioAsset(Repository):
    model = PortfolioAsset


class PortfolioTransaction(Repository):
    model = PortfolioTransaction
