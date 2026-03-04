from fastapi import APIRouter, Depends, status
import httpx

from src.app.api.dependencies.dependency import get_http_client
from src.app.utils.external_api import CMCService

crypto_router = APIRouter(
    prefix="/api/crpyto",
    tags=["crypto"]
)

@crypto_router.get("", status_code=status.HTTP_200_OK)
async def get_crpyto_listing(
    client: httpx.AsyncClient = Depends(get_http_client)
):
    cmc_service = CMCService(client=client)
    return await cmc_service.get_crypto_listing()

@crypto_router.get("/{crypto_currency_id}", status_code=status.HTTP_200_OK)
async def get_crypto_by_id(
    crypto_currency_id: int,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    cmc_service = CMCService(client=client)
    return await cmc_service.get_crypto_by_id(crypto_currency_id=crypto_currency_id)