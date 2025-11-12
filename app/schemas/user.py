from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for User"""
    email: EmailStr  # Validates email format
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for user registration.

    Includes password (will be hashed before storage).
    """
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """Schema for User as stored in database"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    """
    Schema for User in API responses.

    NEVER includes hashed_password!
    """
    pass
