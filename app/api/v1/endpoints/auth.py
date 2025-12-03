from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models import User as UserModel
from app.schemas.user import User, UserCreate
from app.schemas.auth import UserLogin, Token, TokenRefresh
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_access_token
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post('/register', response_model=Token, status_code=201)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register new user"""
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exist")

    hashed_password = hash_password(user.password)

    db_user = UserModel(
        email = user.email,
        hashed_password = hashed_password,
        full_name = user.full_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token =  create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return Token(
        access_token = access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post('/login', response_model=Token, status_code=200)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user"""

    db_user = db.query(UserModel).filter(UserModel.email==login_data.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    if not verify_password(login_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token =  create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})

    return Token(
        access_token = access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.get('/profile', response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user),
):
    """
    Get current authenticated user's profile.

    Returns the user information for the currently logged-in user.
    """
    return current_user

@router.post('/refresh', response_model=Token, status_code=200)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""

    email = decode_access_token(token_data.refresh_token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Verify user still exist
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Generate new tokens
    new_access_token =  create_access_token(data={"sub": email})
    new_refresh_token = create_refresh_token(data={"sub": email})

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )
