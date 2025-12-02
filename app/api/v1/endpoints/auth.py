from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models import User as UserModel
from app.schemas.user import User, UserCreate
from app.schemas.auth import UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token

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

    token =  create_access_token(data={"sub": user.email})

    return Token(
        access_token = token,
        token_type="bearer"
    )

@router.post('/login', response_model=Token, status_code=200)
async def login(
    login_data: UserLogin,
    db: Session=Depends(get_db)
):
    """Login user"""

    db_user = db.query(UserModel).filter(UserModel.email==login_data.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    if not verify_password(login_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = create_access_token(data={"sub": db_user.email})

    return Token(
        access_token = token,
        token_type="bearer"
    )
