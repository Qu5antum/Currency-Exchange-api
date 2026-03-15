from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class MarketSnapshotBase(BaseModel):
    price: float
    volume_24h: float
    percent_change_1h: float
    percent_change_24h: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    currency_id: int

class MarketSnapshotCreate(MarketSnapshotBase):
    timestamp: datetime | None = None

class MarketSnapshotOut(MarketSnapshotBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class QuoteApiUSD(BaseModel):
    price: float
    volume_24h: float
    percent_change_1h: float
    percent_change_24h: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float

class Quote(BaseModel):
    USD: QuoteApiUSD


class CryptoCurrencyBase(BaseModel):
    name: str
    symbol: str
    max_supply: float | None = Field(None)
    circulating_supply: float
    total_supply: float
    cmc_rank: int

class CryptoCurrencyCreate(CryptoCurrencyBase):
    cmc_id: int

class CryptoCurrencyAPIOut(CryptoCurrencyBase):
    id: int
    quote: Quote


class BuyCryptoRequest(BaseModel):
    symbol: str
    amount: float = Field(..., gt=0)
    price: float = Field(..., gt=0)


class SellCryptoRequest(BaseModel):
    symbol: str
    amount: float = Field(..., gt=0)
    price: float = Field(..., gt=0)




