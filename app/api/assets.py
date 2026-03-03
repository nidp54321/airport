from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AssetOut
from app.crud import (
    get_all_assets,
)

router = APIRouter()

# Get all assets
@router.get("/", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return get_all_assets(db)

