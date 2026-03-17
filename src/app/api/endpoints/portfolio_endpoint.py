from fastapi import APIRouter, status, Depends

from src.app.database.db import AsyncSession, get_session
from src.app.database.models import User
from src.app.api.dependencies.dependency import get_current_user
from src.app.api.dependencies.check_role import require_roles
from src.app.service.portfolio_service import PortfolioService
from src.app.api.schemas.crypto_currency import BuyCryptoRequest, SellCryptoRequest
from src.app.api.schemas.portfolio import TransactionRequest, TransactionType


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
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.buy_crypto(portfolio_id=portfolio_id, data=data, user=user)

@portfolio_route.post("/{portfolio_id}/sell", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_201_CREATED)
async def sell_crypto(
    portfolio_id: int,
    data: SellCryptoRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.sell_crypto(portfolio_id=portfolio_id, data=data, user=user)

@portfolio_route.get("/{portfolio_id}/overview", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def portfolio_overview(
    portfolio_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.portfolio_overview(portfolio_id=portfolio_id, user=user)

@portfolio_route.get("/{portfolio_id}/distribution", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def portfolio_distribution(
    portfolio_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.portfolio_distribution(portfolio_id=portfolio_id, user=user)

@portfolio_route.get("/{portfolio_id}/history", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def portfolio_histroy(
    days: int,
    portfolio_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.portfolio_history(days=days, portfolio_id=portfolio_id, user=user)

@portfolio_route.get("{portfolio_id}/transactions", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def transactions(
    portfolio_id: int,
    data: TransactionRequest = Depends(),
    transaction_type: TransactionType | None = None,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    portfolio_service = PortfolioService(session=session)
    return await portfolio_service.get_transactions(portfolio_id=portfolio_id, data=data, transaction_type=transaction_type, user=user)