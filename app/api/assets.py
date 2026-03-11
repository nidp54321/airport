from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import AssetOut
from crud import (
    get_all_assets,
)

router = APIRouter()

# Get all assets
@router.get("/", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return get_all_assets(db)

