from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db, Stock as StockModel
from app.schemas import Stock, StockCreate, StockUpdate

router = APIRouter()

@router.get('/', response_model=List[Stock])
async def get_stocks(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
        """
        Get all stocks.
        """
        stocks = db.query(StockModel).offset(skip).limit(limit).all()

        return stocks

@router.post('/', response_model=Stock, status_code=201)
async def create_stock(
        stock: StockCreate,
        db: Session=Depends(get_db)
):
        """Create new stock"""

        if db.query(StockModel).filter(StockModel.symbol == stock.symbol).first():
                raise HTTPException(status_code=400, detail="Stock already exist in Database")

        db_stock = StockModel(
                **stock.model_dump()
        )

        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        return db_stock

@router.get('/{stock_id}', response_model=Stock)
async def get_stock(
        stock_id: int,
        db: Session = Depends(get_db)
):
        """Get a specific stock by ID"""
        stock = db.get(StockModel, stock_id)

        if not stock:
                raise HTTPException(status_code=404, detail="Stock not found")

        return stock

@router.patch('/{stock_id}', response_model=Stock)
async def update_stock(
        stock_update: StockUpdate,
        stock_id: int,
        db: Session = Depends(get_db)
):
        stock = db.get(StockModel, stock_id)

        if not stock:
                raise HTTPException(status_code=404, detail="Stock not found")

        update_data = stock_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
                setattr(stock, field, value)

        db.commit()
        db.refresh(stock)

        return stock