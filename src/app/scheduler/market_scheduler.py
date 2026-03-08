from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database.db import async_session
from src.app.service.crypto_currency_service import MarketSyncService
from src.app.utils.external_api import CMCServiceApi, get_cmc_service

scheduler = AsyncIOScheduler()


async def sync_market():
    async with async_session() as session:
        cmc_api_service = CMCServiceApi(get_cmc_service)
        service = MarketSyncService(session=session,cmc_api_service=cmc_api_service)
        await service.sync_crypto_currencies(limit=5)

def start_scheduler():

    scheduler.add_job(
        sync_market,
        "interval",
        minutes=5,
        coalesce=True,
        max_instances=1
    )

    scheduler.start()



