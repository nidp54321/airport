from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AssetOut, AssetCreate, AssetUpdate
from app.crud import (
    get_all_assets,
    get_asset_by_id,
    get_assets_by_location,
    get_assets_by_category,
    get_assets_by_status,
    create_asset,
    update_asset,
    delete_asset
)
from app.api.users import get_current_user
from app.models import User

router = APIRouter()


# Get all assets
@router.get("/", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_assets(db)


# Get asset by ID
@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


# Get assets by location
@router.get("/location/{location_id}", response_model=list[AssetOut])
def get_assets_by_location_route(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assets = get_assets_by_location(db, location_id)
    if not assets:
        raise HTTPException(status_code=404, detail="No assets found in this location")
    return assets


# Get assets by category
@router.get("/category/{category}", response_model=list[AssetOut])
def get_assets_by_category_route(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assets = get_assets_by_category(db, category)
    if not assets:
        raise HTTPException(status_code=404, detail="No assets found in this category")
    return assets


# Create new asset
@router.post("/", response_model=AssetOut)
def create_new_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    return create_asset(db, asset)


# Update asset
@router.put("/{asset_id}", response_model=AssetOut)
def update_asset_route(
    asset_id: int,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    db_asset = get_asset_by_id(db, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return update_asset(db, asset_id, asset_data)


# Delete asset
@router.delete("/{asset_id}")
def delete_asset_route(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete assets")

    db_asset = get_asset_by_id(db, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    delete_asset(db, asset_id)
    return {"message": "Asset deleted successfully"}

