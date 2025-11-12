from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


from app.config import settings

# Create sync engine
# echo=True logs all SQL queries
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

# Session factory - creates new database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> Session:
    """
    Dependency function that provides a database session.

    This will be used in FastAPI route dependencies.
    The session is automatically closed after the request.

    Usage in routes:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            # Use db here
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
