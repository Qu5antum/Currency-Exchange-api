from fastapi import Depends
from typing import List, Dict, Any
import httpx

from src.app.api.dependencies.dependency import get_http_client

def get_cmc_api_service(client: httpx.AsyncClient = Depends(get_http_client)):
    return CMCServiceApi(client)

class CMCServiceApi:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_crypto_listing(self, limit: int = 5) -> List[Dict[str, Any]]:
        response = await self.client.get("/v1/cryptocurrency/listings/latest", params={"limit": limit})
        response.raise_for_status()
        result = response.json()

        if result["status"]["error_code"] != 0:
            raise RuntimeError(result["status"]["error_message"])

        return result["data"]
    
    async def get_crypto_by_id(self, crypto_currency_id: int):
        responce = await self.client.get("/v2/cryptocurrency/quotes/latest", params={"id": crypto_currency_id})
        responce.raise_for_status()
        result = responce.json()

        if result["status"]["error_code"] != 0:
            raise RuntimeError(result["status"]["error_message"])

        return result["data"][str(crypto_currency_id)]
    
    

