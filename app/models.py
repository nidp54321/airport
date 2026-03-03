from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=True)
    email = Column(String(150), index=True, nullable=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assets = relationship("Asset", back_populates="created_by_user")
    maintenance_records = relationship("Maintenance", back_populates="assigned_to_user")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True, nullable=False)
    location_type = Column(String(100), nullable=False)  # e.g., Terminal, Runway, Cargo, Office
    capacity = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    assets = relationship("Asset", back_populates="location")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String(100), unique=True, index=True, nullable=False)
    asset_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)  # e.g., Security, Baggage, Ground Equipment
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    status = Column(String(50), default="operational", nullable=False)  # operational, maintenance, inactive
    purchase_date = Column(DateTime, nullable=True)
    purchase_cost = Column(Float, nullable=True)
    serial_number = Column(String(100), nullable=True)
    manufacturer = Column(String(200), nullable=True)
    model = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    location = relationship("Location", back_populates="assets")
    created_by_user = relationship("User", back_populates="assets")
    maintenance_records = relationship("Maintenance", back_populates="asset")


class MaintenanceType(str, enum.Enum):
    """Enum for maintenance types"""
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    INSPECTION = "inspection"
    REPAIR = "repair"


class MaintenanceStatus(str, enum.Enum):
    """Enum for maintenance status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)
    maintenance_id = Column(String(100), unique=True, index=True, nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    maintenance_type = Column(String(50), nullable=False)  # preventive, corrective, inspection, repair
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, in_progress, completed, cancelled
    scheduled_date = Column(DateTime, nullable=False)
    start_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    asset = relationship("Asset", back_populates="maintenance_records")
    assigned_to_user = relationship("User", back_populates="maintenance_records")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(100), unique=True, index=True, nullable=False)
    report_name = Column(String(200), nullable=False)
    report_type = Column(String(100), nullable=False)  # e.g., Analytics, Operations, Performance
    description = Column(Text, nullable=True)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    generated_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    file_path = Column(String(500), nullable=True)
    data_json = Column(Text, nullable=True)  # Store report data as JSON
    is_public = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

