from fastapi import APIRouter, Depends, status
import httpx

from src.app.database.db import AsyncSession, get_session
from src.app.api.dependencies.dependency import get_http_client
from src.app.utils.external_api import CMCServiceApi, get_cmc_api_service
from src.app.service.market_sync_service import MarketSyncService
from src.app.service.crypto_currency_service import CryptoCurrencyService
from src.app.api.dependencies.check_role import require_roles
from src.app.api.schemas.crypto_currency import CryptoCurrencyAPIOut

crypto_router = APIRouter(
    prefix="/api/crypto",
    tags=["crypto"]
)

@crypto_router.get("/api_call", response_model=list[CryptoCurrencyAPIOut], dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def get_crpyto_listing(
    cmc_api_service: CMCServiceApi = Depends(get_cmc_api_service)
):
    return await cmc_api_service.get_crypto_listing()

@crypto_router.get("api_call/{crypto_currency_id}", response_model=CryptoCurrencyAPIOut, dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def get_crypto_by_id(
    crypto_currency_id: int,
    cmc_api_service: CMCServiceApi = Depends(get_cmc_api_service),
):
    return await cmc_api_service.get_crypto_by_id(crypto_currency_id=crypto_currency_id)

@crypto_router.post("/", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_201_CREATED)
async def insert_crypto_in_db(
    cmc_api_service: CMCServiceApi = Depends(get_cmc_api_service),
    session: AsyncSession = Depends(get_session)
):
    market_sync_service = MarketSyncService(session=session, cmc_api_service=cmc_api_service)
    return await market_sync_service.sync_crypto_currencies()

@crypto_router.get("/", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def get_crypto_currencies(
    session: AsyncSession = Depends(get_session)
):
    crypto_currency_service = CryptoCurrencyService(session=session)
    return await crypto_currency_service.get_all_crypto_currencies()

@crypto_router.get("/{symbol}", dependencies=[Depends(require_roles(["USER", "ADMIN"]))], status_code=status.HTTP_200_OK)
async def get_crypto_currencies(
    symbol: str,
    session: AsyncSession = Depends(get_session)
):
    crypto_currency_service = CryptoCurrencyService(session=session)
    return await crypto_currency_service.get_all_crypto_currencies(symbol=symbol)   