from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class StockBase(BaseModel):
    """Base schema for Stock"""
    symbol: str
    name: str
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class StockCreate(StockBase):
    """Schema for creating a stock"""
    pass


class StockUpdate(BaseModel):
    """Schema for updating stock metadata"""
    name: Optional[str] = None
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None


class StockInDB(StockBase):
    """Schema for Stock as stored in database"""
    id: int
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    last_updated: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Stock(StockInDB):
    """Schema for Stock in API responses"""
    pass

