from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Base schema with common fields
class PortfolioBase(BaseModel):
    """Base schema for Portfolio - shared fields"""
    name: str
    description: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    """
    Schema for creating a portfolio.

    Used for POST /portfolios request body.
    Only includes fields the user can set.
    """
    pass  # Inherits name and description from Base


class PortfolioUpdate(BaseModel):
    """
    Schema for updating a portfolio.

    Used for PUT/PATCH /portfolios/{id} request body.
    All fields optional (partial updates allowed).
    """
    name: Optional[str] = None
    description: Optional[str] = None


class PortfolioInDB(PortfolioBase):
    """
    Schema for Portfolio as stored in database.

    Includes database-generated fields like id, timestamps.
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Portfolio(PortfolioInDB):
    """
    Schema for Portfolio in API responses.

    This is what clients receive.
    Can include computed fields, related data, etc.
    """
    pass
