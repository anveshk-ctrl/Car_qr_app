from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Car, IssueType, IssueReport
from ..schemas import IssueReportCreate
from ..services.sms import sms_sender

router = APIRouter(prefix="/report", tags=["public"]) 

templates = Jinja2Templates(directory="app/templates")


@router.get("/{qr_code}", response_class=HTMLResponse)
async def get_report_form(qr_code: str, request: Request, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.qr_code == qr_code, Car.is_active == True).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    issue_types = db.query(IssueType).filter(IssueType.is_active == True).order_by(IssueType.title.asc()).all()
    return templates.TemplateResponse(
        "report_form.html",
        {"request": request, "car": car, "issue_types": issue_types},
    )


@router.post("/{qr_code}")
async def submit_report(qr_code: str, payload: IssueReportCreate, request: Request, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.qr_code == qr_code, Car.is_active == True).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    issue_type = db.query(IssueType).filter(
        IssueType.code == payload.issue_type_code, IssueType.is_active == True
    ).first()
    if not issue_type:
        raise HTTPException(status_code=400, detail="Invalid issue type")

    report = IssueReport(
        car_id=car.id,
        issue_type_id=issue_type.id,
        comment=payload.comment,
        reporter_phone=payload.reporter_phone,
        reporter_ip=request.client.host if request.client else None,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    try:
        sms_sender.send(
            to_e164=car.owner_phone_e164,
            body=f"Car issue reported: {issue_type.title}. QR: {car.qr_code}. Comment: {payload.comment or '-'}",
        )
    except Exception:
        pass

    return {"ok": True, "report_id": report.id}
