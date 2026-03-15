from sqlalchemy import String, Integer, Column, ForeignKey, Table, Float, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

from src.app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True)

    roles: Mapped[list["Role"]] = relationship(
        secondary="user_roles",
        back_populates="users"
    )

    portfolios: Mapped[list["Portfolio"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)

    users: Mapped[list["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles"
    )


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class CryptoCurrency(Base):
    __tablename__ = "crypto_currencies" 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cmc_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    symbol: Mapped[str] = mapped_column(String, index=True)
    max_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    circulating_supply: Mapped[float] = mapped_column(Float)
    total_supply: Mapped[float] = mapped_column(Float)
    cmc_rank: Mapped[int] = mapped_column(Integer)

    snapshots: Mapped[list["MarketSnapshot"]] = relationship(back_populates="crypto_currency", cascade="all, delete-orphan")
    portfolio_assets: Mapped[list["PortfolioAsset"]] = relationship(back_populates="crypto_currency")
    portfolio_transactions: Mapped[list["PortfolioTransaction"]] = relationship(back_populates="crypto_currency")


class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    price: Mapped[float] = mapped_column(Float)
    volume_24h: Mapped[float] = mapped_column(Float)
    percent_change_1h: Mapped[float] = mapped_column(Float)
    percent_change_24h: Mapped[float] = mapped_column(Float)
    market_cap: Mapped[float] = mapped_column(Float)
    market_cap_dominance: Mapped[float] = mapped_column(Float)
    fully_diluted_market_cap: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.UTC),
        index=True
    )

    currency_id: Mapped[int] = mapped_column(Integer, ForeignKey("crypto_currencies.id"), index=True, nullable=False)
    crypto_currency: Mapped["CryptoCurrency"] = relationship(back_populates="snapshots")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.UTC), 
        index=True
    )

    user: Mapped["User"] = relationship(back_populates="portfolios")
    assets: Mapped[list["PortfolioAsset"]] = relationship(back_populates="portfolio",cascade="all, delete-orphan")
    transactions: Mapped[list["PortfolioTransaction"]] = relationship(back_populates="portfolio",cascade="all, delete-orphan")

class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float)
    avg_buy_price: Mapped[float] = mapped_column(Float)

    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolios.id"), index=True, nullable=False)
    crypto_currency_id: Mapped[int] = mapped_column(Integer, ForeignKey("crypto_currencies.id"), index=True, nullable=False)
    portfolio: Mapped["Portfolio"] = relationship(back_populates="assets")
    crypto_currency: Mapped["CryptoCurrency"] = relationship(back_populates="portfolio_assets")


class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.UTC), 
        index=True
    )

    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolios.id"), index=True, nullable=False)
    crypto_currency_id: Mapped[int] = mapped_column(Integer, ForeignKey("crypto_currencies.id"), index=True, nullable=False)
    portfolio: Mapped["Portfolio"] = relationship(back_populates="transactions")
    crypto_currency: Mapped["CryptoCurrency"] = relationship(back_populates="portfolio_transactions")

__table_args__ = (
    UniqueConstraint("portfolio_id", "crypto_currency_id"),
)

    
    





