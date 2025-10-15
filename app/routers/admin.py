from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Car, IssueType
from ..schemas import CarCreate, CarRead, IssueTypeCreate, IssueTypeRead

router = APIRouter(prefix="/admin", tags=["admin"]) 


@router.post("/cars", response_model=CarRead)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    exists = db.query(Car).filter(Car.qr_code == car.qr_code).first()
    if exists:
        raise HTTPException(status_code=400, detail="QR already registered")

    obj = Car(qr_code=car.qr_code, owner_name=car.owner_name, owner_phone_e164=car.owner_phone_e164)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/cars", response_model=list[CarRead])
def list_cars(db: Session = Depends(get_db)):
    return db.query(Car).order_by(Car.id.desc()).all()


@router.post("/issue-types", response_model=IssueTypeRead)
def create_issue_type(item: IssueTypeCreate, db: Session = Depends(get_db)):
    exists = db.query(IssueType).filter(IssueType.code == item.code).first()
    if exists:
        raise HTTPException(status_code=400, detail="Issue code exists")

    obj = IssueType(code=item.code, title=item.title, description=item.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/issue-types", response_model=list[IssueTypeRead])
def list_issue_types(db: Session = Depends(get_db)):
    return db.query(IssueType).filter(IssueType.is_active == True).order_by(IssueType.title.asc()).all()
