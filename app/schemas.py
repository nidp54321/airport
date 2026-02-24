from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ========================
# User Schemas
# ========================

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str = "user"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


# ========================
# Location Schemas
# ========================

class LocationBase(BaseModel):
    name: str
    location_type: str
    capacity: Optional[int] = None
    description: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    location_type: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class LocationOut(BaseModel):
    id: int
    name: str
    location_type: str
    capacity: Optional[int]
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ========================
# Asset Schemas
# ========================

class AssetBase(BaseModel):
    asset_id: str
    asset_name: str
    category: str
    location_id: int
    status: str = "operational"


class AssetCreate(AssetBase):
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[int] = None


class AssetUpdate(BaseModel):
    asset_name: Optional[str] = None
    category: Optional[str] = None
    location_id: Optional[int] = None
    status: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None


class AssetOut(BaseModel):
    id: int
    asset_id: str
    asset_name: str
    category: str
    location_id: int
    status: str
    purchase_date: Optional[datetime]
    purchase_cost: Optional[float]
    serial_number: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    description: Optional[str]
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ========================
# Maintenance Schemas
# ========================

class MaintenanceBase(BaseModel):
    maintenance_id: str
    asset_id: int
    maintenance_type: str
    scheduled_date: datetime
    status: str = "scheduled"


class MaintenanceCreate(MaintenanceBase):
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None


class MaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    status: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None


class MaintenanceOut(BaseModel):
    id: int
    maintenance_id: str
    asset_id: int
    maintenance_type: str
    status: str
    scheduled_date: datetime
    start_date: Optional[datetime]
    completion_date: Optional[datetime]
    assigned_to: Optional[int]
    description: Optional[str]
    notes: Optional[str]
    estimated_cost: Optional[float]
    actual_cost: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ========================
# Report Schemas
# ========================

class ReportBase(BaseModel):
    report_id: str
    report_name: str
    report_type: str


class ReportCreate(ReportBase):
    description: Optional[str] = None
    generated_by: Optional[int] = None
    file_path: Optional[str] = None
    data_json: Optional[str] = None
    is_public: bool = False


class ReportUpdate(BaseModel):
    report_name: Optional[str] = None
    report_type: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    data_json: Optional[str] = None
    is_public: Optional[bool] = None


class ReportOut(BaseModel):
    id: int
    report_id: str
    report_name: str
    report_type: str
    description: Optional[str]
    generated_by: Optional[int]
    generated_date: datetime
    file_path: Optional[str]
    data_json: Optional[str]
    is_public: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

