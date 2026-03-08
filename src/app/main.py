from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, asyncio, httpx
from contextlib import asynccontextmanager

from src.app.database.db import init_models
from src.app.core.config import settings
from src.app.api.endpoints.user_endpoint import user_router
from src.app.api.endpoints.crypto_currency import crypto_router
from src.app.scheduler.market_scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        base_url="https://pro-api.coinmarketcap.com",
        headers={
            "X-CMC_PRO_API_KEY": settings.CMC_API_KEY
        },
        timeout=10.0
    )

    yield 

    await app.state.http_client.aclose()

app = FastAPI(
    lifespan=lifespan,
    title = settings.APP_NAME,
    debug=settings.debug,
    docs_url="/docs"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(user_router)
app.include_router(crypto_router)


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(
        "src.app.main:app", host="127.0.0.1", port=8000, reload=True
)
