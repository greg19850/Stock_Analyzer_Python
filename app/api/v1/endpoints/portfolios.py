from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.db.models import Portfolio as PortfolioModel, User as UserModel
from app.schemas import Portfolio, PortfolioCreate, PortfolioUpdate
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Portfolio])
async def get_portfolios(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Get all portfolios.

    Test endpoint.
    """
    portfolios = db.query(PortfolioModel).offset(skip).limit(limit).all()
    return portfolios


@router.get("/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(
        portfolio_id: int,
        db: Session = Depends(get_db)
):
    """Get a specific portfolio by ID"""
    portfolio = db.get(PortfolioModel, portfolio_id)


    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio


@router.post("/", response_model=Portfolio, status_code=201)
async def create_portfolio(
        portfolio: PortfolioCreate,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """
    Create a new portfolio.
    """
    db_portfolio = PortfolioModel(
        **portfolio.model_dump(),
        user_id = current_user.id
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.patch("/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(
        portfolio_update: PortfolioUpdate,
        portfolio_id: int,
        db: Session = Depends(get_db)
):
    portfolio = db.get(PortfolioModel, portfolio_id)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Get only the fields user wants to update
    update_data = portfolio_update.model_dump(exclude_unset=True)

    # Update the existing holding object
    for field, value in update_data.items():
        setattr(portfolio, field, value)

    db.commit()
    db.refresh(portfolio)

    return portfolio

@router.delete("/{portfolio_id}", status_code=204)
async def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    portfolio = db.get(PortfolioModel, portfolio_id)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(portfolio)
    db.commit()

    return None