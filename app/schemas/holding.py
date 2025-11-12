from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class HoldingBase(BaseModel):
    """Base schema for Holding"""
    stock_id: int
    quantity: float = Field(gt=0, description="Number of shares (must be positive)")
    average_purchase_price: float = Field(gt=0, description="Average price per share")
    purchase_date: datetime
    notes: Optional[str] = None


class HoldingCreate(HoldingBase):
    """
    Schema for creating a holding.

    portfolio_id is in the URL path, not request body.
    """
    pass


class HoldingUpdate(BaseModel):
    """Schema for updating a holding"""
    quantity: Optional[float] = Field(None, gt=0)
    average_purchase_price: Optional[float] = Field(None, gt=0)
    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None


class HoldingInDB(HoldingBase):
    """Schema for Holding as stored in database"""
    id: int
    portfolio_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Holding(HoldingInDB):
    """
    Schema for Holding in API responses.

    Can include nested stock data for convenience.
    """
    pass


class HoldingWithStock(Holding):
    """
    Extended holding schema with stock details.

    Useful for portfolio views where you want stock info
    without making separate API calls.
    """
    stock: "Stock"

# Import at the end to resolve forward reference
from app.schemas.stock import Stock

# Update forward references
HoldingWithStock.model_rebuild()
