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

router = APIRouter()


# Get all reports
@router.get("/", response_model=list[ReportOut])
def list_reports(db: Session = Depends(get_db)):
    return get_all_reports(db)


# Get public reports
@router.get("/public/", response_model=list[ReportOut])
def list_public_reports(db: Session = Depends(get_db)):
    return get_public_reports(db)


# Get report by ID
@router.get("/{report_id}", response_model=ReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# Get reports by type
@router.get("/type/{report_type}", response_model=list[ReportOut])
def get_reports_by_type_route(
    report_type: str,
    db: Session = Depends(get_db),
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
):
    return create_report(db, report)


# Update report
@router.put("/{report_id}", response_model=ReportOut)
def update_report_route(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
):
    db_report = get_report_by_id(db, report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")

    return update_report(db, report_id, report_data)


# Delete report
@router.delete("/{report_id}")
def delete_report_route(
    report_id: int,
    db: Session = Depends(get_db),
):
    db_report = get_report_by_id(db, report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")

    delete_report(db, report_id)
    return {"message": "Report deleted successfully"}
