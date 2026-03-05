from sqlalchemy import String, Integer, Column, ForeignKey, Table, Float, DateTime, BigInteger
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


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cmc_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    symbol: Mapped[str] = mapped_column(String, index=True)
    max_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    circulating_supply: Mapped[float] = mapped_column(Float)
    total_supply: Mapped[float] = mapped_column(Float)
    cmc_rank: Mapped[int] = mapped_column(Integer)

    snapshots: Mapped[list["MarketSnapshot"]] = relationship(back_populates="currency", cascade="all, delete-orphan")


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
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), index=True)

    currency_id: Mapped[int] = mapped_column(Integer, ForeignKey("currencies.id"), index=True, nullable=False)
    currency: Mapped["Currency"] = relationship(back_populates="snapshot")







