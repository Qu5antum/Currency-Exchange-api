from pydantic import BaseModel

class PortfolioOut(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        from_attributes = True

        