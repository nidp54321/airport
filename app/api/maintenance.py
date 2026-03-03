from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MaintenanceOut, MaintenanceCreate, MaintenanceUpdate
from app.crud import (
    get_all_maintenance,
    get_maintenance_by_id,
    get_maintenance_by_asset,
    get_maintenance_by_status,
    get_maintenance_by_assigned_user,
    create_maintenance,
    update_maintenance,
    delete_maintenance
)

router = APIRouter()


# Get all maintenance records
@router.get("/", response_model=list[MaintenanceOut])
def list_maintenance(db: Session = Depends(get_db)):
    return get_all_maintenance(db)


# Get maintenance by ID
@router.get("/{maintenance_id}", response_model=MaintenanceOut)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = get_maintenance_by_id(db, maintenance_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return maintenance


# Get maintenance by asset
@router.get("/asset/{asset_id}", response_model=list[MaintenanceOut])
def get_maintenance_by_asset_route(
    asset_id: int,
    db: Session = Depends(get_db),
):
    maintenance = get_maintenance_by_asset(db, asset_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="No maintenance records found for this asset")
    return maintenance


# Get maintenance by status
@router.get("/status/{status}", response_model=list[MaintenanceOut])
def get_maintenance_by_status_route(
    status: str,
    db: Session = Depends(get_db),
):
    maintenance = get_maintenance_by_status(db, status)
    if not maintenance:
        raise HTTPException(status_code=404, detail="No maintenance records found with this status")
    return maintenance


# Get maintenance assigned to user
@router.get("/assigned/{user_id}", response_model=list[MaintenanceOut])
def get_maintenance_assigned_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    maintenance = get_maintenance_by_assigned_user(db, user_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="No maintenance records assigned to this user")
    return maintenance


# Create new maintenance record
@router.post("/", response_model=MaintenanceOut)
def create_new_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    return create_maintenance(db, maintenance)


# Update maintenance record
@router.put("/{maintenance_id}", response_model=MaintenanceOut)
def update_maintenance_route(
    maintenance_id: int,
    maintenance_data: MaintenanceUpdate,
    db: Session = Depends(get_db),
):
    db_maintenance = get_maintenance_by_id(db, maintenance_id)
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    return update_maintenance(db, maintenance_id, maintenance_data)


# Delete maintenance record
@router.delete("/{maintenance_id}")
def delete_maintenance_route(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    db_maintenance = get_maintenance_by_id(db, maintenance_id)
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    delete_maintenance(db, maintenance_id)
    return {"message": "Maintenance record deleted successfully"}
