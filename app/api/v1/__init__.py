from fastapi import APIRouter
from app.api.v1.endpoints import portfolios, holdings, stocks, auth

api_router = APIRouter()

api_router.include_router(
    portfolios.router,
    prefix="/portfolios",
    tags=["portfolios"]
)

api_router.include_router(
    holdings.router,
    prefix="/portfolios/{portfolio_id}/holdings",
    tags=["holdings"]
)

api_router.include_router(
    stocks.router,
    prefix="/stocks",
    tags=["stocks"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)