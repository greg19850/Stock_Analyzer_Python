from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Uses pydantic-settings to automatically load from .env file
    and validate types. This is a best practice for managing config.
    """

    # Application
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Stock API
    ALPHA_VANTAGE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a single instance to use throughout the app
settings = Settings()