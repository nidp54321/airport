from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import LocationOut, LocationCreate, LocationUpdate
from crud import (
    get_all_locations,
    get_location_by_id,
    create_location,
    update_location,
    delete_location
)

router = APIRouter()

@router.get("/", response_model=list[LocationOut])
def list_locations(db: Session = Depends(get_db)):
    return get_all_locations(db)

@router.get("/{location_id}", response_model=LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = get_location_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.post("/", response_model=LocationOut)
def create_new_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
):
    return create_location(db, location)

@router.put("/{location_id}", response_model=LocationOut)
def update_location_route(
    location_id: int,
    location_data: LocationUpdate,
    db: Session = Depends(get_db),
):
    db_location = get_location_by_id(db, location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    return update_location(db, location_id, location_data)

@router.delete("/{location_id}")
def delete_location_route(
    location_id: int,
    db: Session = Depends(get_db),
):
    db_location = get_location_by_id(db, location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    delete_location(db, location_id)
    return {"message": "Location deleted successfully"}
