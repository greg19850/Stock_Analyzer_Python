from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models import User as UserModel
from app.core.security import decode_access_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
)-> UserModel:
    """
    Dependency to get the current authenticated user from JWT token.

    Extracts and validates the JWT token from the Authorization header.
    Returns the user if valid, raises 401 if invalid.
    """

    token = credentials.access_token
    email = decode_access_token(token)

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = db.query(UserModel).filter(UserModel.email==email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    return user