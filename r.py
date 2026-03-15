import httpx
import asyncio

async def test():
    async with httpx.AsyncClient(
        base_url="https://pro-api.coinmarketcap.com",
        headers={"X-CMC_PRO_API_KEY": "YOUR_KEY"},
        trust_env=False
    ) as client:
        r = await client.get("/v1/cryptocurrency/listings/latest", params={"limit": 5})
        print(r.status_code)
        print(r.text)

asyncio.run(test())