from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db import get_db, Holding as HoldingModel, Portfolio as PortfolioModel
from app.schemas import Holding, HoldingCreate, HoldingUpdate

router = APIRouter()

@router.get("/", response_model=List[Holding])
async def get_holdings(
        portfolio_id: int = Path(..., description="Portfolio ID"),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Get all holdings.

    - portfolio_id: The portfolio to get holdings from (from URL)
    - skip: number of records to skip (for pagination)
    - limit: max number of records to return
    """
    portfolio = db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Get holdings for this portfolio only
    holdings = db.query(HoldingModel).filter(
        HoldingModel.portfolio_id == portfolio_id
    ).offset(skip).limit(limit).all()

    return holdings

@router.post("/", response_model=Holding, status_code=201)
async def create_holding(
        holding: HoldingCreate,
        portfolio_id: int = Path(..., description="The portfolio ID"),
        db: Session = Depends(get_db)
):
    """
    Create a new holding in a specific portfolio.

    - portfolio_id: The portfolio to add this holding to (from URL)
    - holding: The holding data (stock_id, quantity, price, etc.)
    """

    portfolio = db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    """ Create new holding """
    db_holding = HoldingModel(
        **holding.model_dump(),
        portfolio_id=portfolio_id
    )
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

@router.get("/{holding_id}", response_model=Holding)
async def get_holding(
        portfolio_id: int = Path(..., description="The portfolio ID"),
        holding_id: int = Path(..., description="The holding ID"),
        db: Session = Depends(get_db)
):
    """
    Get a specific holding from a specific portfolio.

    - portfolio_id: The portfolio ID (from URL)
    - holding_id: The holding ID (from URL)
    """
    holding = db.query(HoldingModel).filter(
        HoldingModel.id == holding_id,
        HoldingModel.portfolio_id == portfolio_id
    ).first()

    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    return holding

@router.patch("/{holding_id}", response_model=Holding)
async def update_holding(
        holding_update: HoldingUpdate,
        portfolio_id: int = Path(..., description="Portfolio ID"),
        holding_id: int = Path(..., description="Holding ID"),
        db: Session = Depends(get_db)
):
    holding = db.query(HoldingModel).filter(
        HoldingModel.id == holding_id,
        HoldingModel.portfolio_id == portfolio_id
    ).first()

    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    # Get only the fields user wants to update
    update_data = holding_update.model_dump(exclude_unset=True)

    # Update the existing holding object
    for field, value in update_data.items():
        setattr(holding, field, value)

    # Save to database
    db.commit()
    db.refresh(holding)

    return holding

@router.delete("/{holding_id}", status_code=204)
async def delete_holding(
        portfolio_id: int = Path(...),
        holding_id: int = Path(...),
        db: Session = Depends(get_db)
):
    holding = db.query(HoldingModel).filter(
        HoldingModel.id == holding_id,
        HoldingModel.portfolio_id == portfolio_id
    ).first()

    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")

    db.delete(holding)
    db.commit()

    return None

