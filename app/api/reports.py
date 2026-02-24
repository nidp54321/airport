from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ReportOut, ReportCreate, ReportUpdate
from app.crud import (
    get_all_reports,
    get_report_by_id,
    get_reports_by_type,
    get_public_reports,
    create_report,
    update_report,
    delete_report
)
from app.api.users import get_current_user
from app.models import User

router = APIRouter()


# Get all reports
@router.get("/", response_model=list[ReportOut])
def list_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_reports(db)


# Get public reports
@router.get("/public/", response_model=list[ReportOut])
def list_public_reports(db: Session = Depends(get_db)):
    return get_public_reports(db)


# Get report by ID
@router.get("/{report_id}", response_model=ReportOut)
def get_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.is_public and report.generated_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    return report


# Get reports by type
@router.get("/type/{report_type}", response_model=list[ReportOut])
def get_reports_by_type_route(
    report_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reports = get_reports_by_type(db, report_type)
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found with this type")
    return reports


# Create new report
@router.post("/", response_model=ReportOut)
def create_new_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "manager", "analyst"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    return create_report(db, report)


# Update report
@router.put("/{report_id}", response_model=ReportOut)
def update_report_route(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_report = get_report_by_id(db, report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")

    if db_report.generated_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    return update_report(db, report_id, report_data)


# Delete report
@router.delete("/{report_id}")
def delete_report_route(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_report = get_report_by_id(db, report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")

    if db_report.generated_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    delete_report(db, report_id)
    return {"message": "Report deleted successfully"}

