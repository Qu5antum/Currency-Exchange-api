from fastapi import HTTPException, status

from src.app.database.db import AsyncSession
from src.app.database.models import Portfolio, PortfolioAsset, PortfolioTransaction, User
from src.app.repositories.portfolio_repository import PortfolioRepostory


class PortfolioService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.portfolio_repo = PortfolioRepostory(session=self.session)

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


