from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.database import engine
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application lifespan events.

    Code before 'yield' runs on startup.
    Code after 'yield' runs on shutdown.
    """
    # Startup logic
    print(f"🚀 Starting {settings.PROJECT_NAME}")


    yield # Application runs here, handling requests

    # Shutdown logic
    print(f"👋 Shutting down {settings.PROJECT_NAME}")
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",  # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",  # ReDoc at http://localhost:8000/redoc
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """
    Root endpoint - basic health check.

    Notice 'async def' - FastAPI supports async/await natively.
    Use async when doing I/O operations (database, API calls).
    """
    return {
        "message": "Investment Portfolio Analyzer API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns service status.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }




