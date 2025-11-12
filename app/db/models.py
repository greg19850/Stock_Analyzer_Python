from operator import index

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import enum

from app.db.database import Base

class User(Base):
    """
    User model - represents registered users.

    Relationships:
    - portfolios: All portfolios owned by this user
    - alerts: All alerts created by this user
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    # Relationships
    portfolios = relationship("Portfolio", back_populates="owner", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")

class Portfolio(Base):
    """
    Portfolio model - collection of stock holdings.

    Relationships:
    - owner: The user who owns this portfolio
    - holdings: All stock holdings in this portfolio
    """
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    owner = relationship("User", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")

class Stock(Base):
    """
    Stock model - master data for stocks.

    This stores metadata about stocks (symbol, name, etc.)
    Actual holdings and prices are in separate tables.

    Relationships:
    - holdings: All holdings of this stock across portfolios
    - price_history: Historical price data
    """
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    exchange = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)

    # Cached metrics (updated by background jobs)
    current_price = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)

    last_updated = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationships
    holdings = relationship("Holding", back_populates="stock")
    price_history = relationship("PriceHistory", back_populates="stock", cascade="all, delete-orphan")


class Holding(Base):
    """
    Holding model - represents ownership of stock in a portfolio.

    Junction table between Portfolio and Stock with additional data.

    Relationships:
    - portfolio: The portfolio containing this holding
    - stock: The stock being held
    - alerts: Alerts set on this holding
    """
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)

    quantity = Column(Float, nullable=False)
    average_purchase_price = Column(Float, nullable=False)
    purchase_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    stock = relationship("Stock", back_populates="holdings")
    alerts = relationship("Alert", back_populates="holding", cascade="all, delete-orphan")


class PriceHistory(Base):
    """
    Price history model - stores historical stock prices.

    Updated by background jobs pulling from stock APIs.
    Used for charts, analysis, and calculating returns.
    """
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)

    date = Column(DateTime(timezone=True), nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    # Relationships
    stock = relationship("Stock", back_populates="price_history")

class ConditionType(str, enum.Enum):
    """Alert condition types"""
    PRICE_ABOVE = "price_above"
    PRICE_BELOW = "price_below"
    PERCENT_CHANGE_UP = "percent_change_up"
    PERCENT_CHANGE_DOWN = "percent_change_down"

class Alert(Base):
    """
    Alert model - user-defined alerts for price movements.

    Evaluated by background jobs, triggers notifications.

    Relationships:
    - user: The user who created this alert
    - holding: The holding this alert monitors
    """
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    holding_id = Column(Integer, ForeignKey("holdings.id", ondelete="CASCADE"), nullable=False)

    condition_type = Column(Enum(ConditionType), nullable=False)
    threshold_value = Column(Float, nullable=False)

    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    user = relationship("User", back_populates="alerts")
    holding = relationship("Holding", back_populates="alerts")



