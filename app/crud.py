from sqlalchemy.orm import Session
from app.models import User, Asset, Location, Maintenance, Report
from app.auth import get_password_hash, verify_password

# ========================
# User CRUD Operations
# ========================

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user_data):
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=getattr(user_data, "email", None),
        hashed_password=hashed_password,
        full_name=getattr(user_data, "full_name", None),
        role=getattr(user_data, "role", "user")
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ========================
# Location CRUD Operations
# ========================

def get_location_by_id(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()


def get_location_by_name(db: Session, name: str):
    return db.query(Location).filter(Location.name == name).first()


def get_all_locations(db: Session):
    return db.query(Location).filter(Location.is_active == True).all()


def create_location(db: Session, location_data):
    db_location = Location(
        name=location_data.name,
        location_type=location_data.location_type,
        capacity=getattr(location_data, "capacity", None),
        description=getattr(location_data, "description", None)
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(db: Session, location_id: int, location_data):
    db_location = get_location_by_id(db, location_id)
    if db_location:
        for key, value in location_data.dict(exclude_unset=True).items():
            setattr(db_location, key, value)
        db.commit()
        db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: int):
    db_location = get_location_by_id(db, location_id)
    if db_location:
        db_location.is_active = False
        db.commit()
    return db_location


# ========================
# Asset CRUD Operations
# ========================

def get_asset_by_id(db: Session, asset_id: int):
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_asset_by_asset_id(db: Session, asset_id: str):
    return db.query(Asset).filter(Asset.asset_id == asset_id).first()


def get_all_assets(db: Session):
    return db.query(Asset).all()


def get_assets_by_location(db: Session, location_id: int):
    return db.query(Asset).filter(Asset.location_id == location_id).all()


def get_assets_by_category(db: Session, category: str):
    return db.query(Asset).filter(Asset.category == category).all()


def get_assets_by_status(db: Session, status: str):
    return db.query(Asset).filter(Asset.status == status).all()


def create_asset(db: Session, asset_data):
    db_asset = Asset(
        asset_id=asset_data.asset_id,
        asset_name=asset_data.asset_name,
        category=asset_data.category,
        location_id=asset_data.location_id,
        status=getattr(asset_data, "status", "operational"),
        purchase_date=getattr(asset_data, "purchase_date", None),
        purchase_cost=getattr(asset_data, "purchase_cost", None),
        serial_number=getattr(asset_data, "serial_number", None),
        manufacturer=getattr(asset_data, "manufacturer", None),
        model=getattr(asset_data, "model", None),
        description=getattr(asset_data, "description", None),
        created_by=getattr(asset_data, "created_by", None)
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def update_asset(db: Session, asset_id: int, asset_data):
    db_asset = get_asset_by_id(db, asset_id)
    if db_asset:
        for key, value in asset_data.dict(exclude_unset=True).items():
            setattr(db_asset, key, value)
        db.commit()
        db.refresh(db_asset)
    return db_asset


def delete_asset(db: Session, asset_id: int):
    db_asset = get_asset_by_id(db, asset_id)
    if db_asset:
        db.delete(db_asset)
        db.commit()
    return db_asset


# ========================
# Maintenance CRUD Operations
# ========================

def get_maintenance_by_id(db: Session, maintenance_id: int):
    return db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()


def get_all_maintenance(db: Session):
    return db.query(Maintenance).all()


def get_maintenance_by_asset(db: Session, asset_id: int):
    return db.query(Maintenance).filter(Maintenance.asset_id == asset_id).all()


def get_maintenance_by_status(db: Session, status: str):
    return db.query(Maintenance).filter(Maintenance.status == status).all()


def get_maintenance_by_assigned_user(db: Session, user_id: int):
    return db.query(Maintenance).filter(Maintenance.assigned_to == user_id).all()


def create_maintenance(db: Session, maintenance_data):
    db_maintenance = Maintenance(
        maintenance_id=maintenance_data.maintenance_id,
        asset_id=maintenance_data.asset_id,
        maintenance_type=maintenance_data.maintenance_type,
        status=getattr(maintenance_data, "status", "scheduled"),
        scheduled_date=maintenance_data.scheduled_date,
        start_date=getattr(maintenance_data, "start_date", None),
        completion_date=getattr(maintenance_data, "completion_date", None),
        assigned_to=getattr(maintenance_data, "assigned_to", None),
        description=getattr(maintenance_data, "description", None),
        notes=getattr(maintenance_data, "notes", None),
        estimated_cost=getattr(maintenance_data, "estimated_cost", None),
        actual_cost=getattr(maintenance_data, "actual_cost", None)
    )
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


def update_maintenance(db: Session, maintenance_id: int, maintenance_data):
    db_maintenance = get_maintenance_by_id(db, maintenance_id)
    if db_maintenance:
        for key, value in maintenance_data.dict(exclude_unset=True).items():
            setattr(db_maintenance, key, value)
        db.commit()
        db.refresh(db_maintenance)
    return db_maintenance


def delete_maintenance(db: Session, maintenance_id: int):
    db_maintenance = get_maintenance_by_id(db, maintenance_id)
    if db_maintenance:
        db.delete(db_maintenance)
        db.commit()
    return db_maintenance


# ========================
# Report CRUD Operations
# ========================

def get_report_by_id(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()


def get_all_reports(db: Session):
    return db.query(Report).all()


def get_reports_by_type(db: Session, report_type: str):
    return db.query(Report).filter(Report.report_type == report_type).all()


def get_public_reports(db: Session):
    return db.query(Report).filter(Report.is_public == True).all()


def create_report(db: Session, report_data):
    db_report = Report(
        report_id=report_data.report_id,
        report_name=report_data.report_name,
        report_type=report_data.report_type,
        description=getattr(report_data, "description", None),
        generated_by=getattr(report_data, "generated_by", None),
        file_path=getattr(report_data, "file_path", None),
        data_json=getattr(report_data, "data_json", None),
        is_public=getattr(report_data, "is_public", False)
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def update_report(db: Session, report_id: int, report_data):
    db_report = get_report_by_id(db, report_id)
    if db_report:
        for key, value in report_data.dict(exclude_unset=True).items():
            setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)
    return db_report


def delete_report(db: Session, report_id: int):
    db_report = get_report_by_id(db, report_id)
    if db_report:
        db.delete(db_report)
        db.commit()
    return db_report

