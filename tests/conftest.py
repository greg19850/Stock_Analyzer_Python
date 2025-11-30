import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from contextlib import asynccontextmanager
from sqlalchemy.pool import StaticPool

from app.db.models import User, Portfolio, Stock, Holding, PriceHistory, Alert

from app.main import app
from app.db.database import Base
from app.db import get_db



engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)



@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database for each test.
    This runs before each test and tears down after.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create db session
    db = TestingSessionLocal()

    try:
        yield db # This is where the test runs
    finally:
        db.close()

        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """
    Create a test client that uses the test database.
    """
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    @asynccontextmanager
    async def no_op_lifespan(app):
        yield

    original_lifespan = app.router.lifespan_context
    app.router.lifespan_context = no_op_lifespan

    with TestClient(app) as test_client:
        yield test_client

    # Restore and clean up
    app.router.lifespan_context = original_lifespan
    app.dependency_overrides.clear()