import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def hash_password(password: str)-> str:
    """
    Hash a password using bcrypt

    Args:
        password (str): plain text password

    Returns:
        str: Hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str)-> bool:
    """
    Verify password against a hash.

    Args:
        plain_password (str): Plain text password to check
        hashed_password (str): Hashed password from database

    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None)-> str:
    """
    Create a JWT access token

    Args:
        data (dict): Dictionary of data to encode in the token (usually {"sub": user_email})
        expires_delta (Optional[timedelta], optional): Optional custom expiration time. Defaults to None.

    Returns:
        str: Encoded JWT token as string
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiration to toke data
    to_encode.update({"exp": expire})

    # Encode JWT token
    token =jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str)-> Optional[str]:
    """
    Decode and validate a JWT token

    Args:
        token (str): JWT token string

    Returns:
        Optional[str]: Email from token if valid, None if invalid
    """
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #Extract the email from the "sub" field
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None