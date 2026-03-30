from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx

from src.app.database.db import async_session
from src.app.core.config import settings
from src.app.service.market_sync_service import MarketSyncService
from src.app.utils.external_api import CMCServiceApi, get_cmc_api_service

scheduler = AsyncIOScheduler()


async def sync_market():
    async with async_session() as session:
        async with httpx.AsyncClient(
            base_url="https://pro-api.coinmarketcap.com",
            headers={"X-CMC_PRO_API_KEY": settings.CMC_API_KEY},
            timeout=10.0,
        ) as http_client:
            cmc_api_service = CMCServiceApi(http_client)
            service = MarketSyncService(session=session, cmc_api_service=cmc_api_service)
            await service.sync_market_snapshots(limit=5)

def start_scheduler():

    scheduler.add_job(
        sync_market,
        "interval",
        minutes=60,
        coalesce=True,
        max_instances=1
    )

    scheduler.start()



