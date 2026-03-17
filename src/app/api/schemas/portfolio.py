from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class PortfolioOut(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        from_attributes = True


class TransactionRequest(BaseModel):
    symbol: str | None = Field(None)
    date_from: datetime | None = Field(None)
    date_to: datetime | None = Field(None)

class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"