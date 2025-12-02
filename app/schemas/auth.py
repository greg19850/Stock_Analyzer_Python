from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    """Base schema for User Login"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Base schema for Token"""
    access_token: str
    token_type: str