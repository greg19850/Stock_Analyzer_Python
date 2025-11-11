from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.testing import future

from app.config import settings

# Create async engine
# echo=True logs all SQL queries
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# Session factory - creates new database sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_= AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency function that provides a database session.

    This will be used in FastAPI route dependencies.
    The session is automatically closed after the request.

    Usage in routes:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            # Use db here
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await  session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
