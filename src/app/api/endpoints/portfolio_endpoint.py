from fastapi import APIRouter, status, Depends

from src.app.database.db import AsyncSession, get_session
from src.app.database.models import User
from src.app.api.dependencies.dependency import get_current_user
from src.app.api.dependencies.check_role import require_roles
from src.app.service.portfolio_service import PortfolioService
from src.app.api.schemas.crypto_currency import BuyCryptoRequest, SellCryptoRequest


portfolio_route = APIRouter(
    prefix="/api/portfolio",
    tags=["portfolios"]
)

@portfolio_route.post("/create", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    name: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.add_portfolio_for_user(name=name, user=user)

@portfolio_route.post("/{portfolio_id}/buy", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_201_CREATED)
async def buy_crypto(
    portfolio_id: int,
    data: BuyCryptoRequest,
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.buy_crypto(portfolio_id=portfolio_id, data=data)

@portfolio_route.post("/{portfolio_id}/sell", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_201_CREATED)
async def sell_crypto(
    portfolio_id: int,
    data: SellCryptoRequest,
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.sell_crypto(portfolio_id=portfolio_id, data=data)