from fastapi import APIRouter
from app.api.v1.endpoints import portfolios, holdings

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
