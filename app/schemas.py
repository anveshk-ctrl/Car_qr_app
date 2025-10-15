from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class CarCreate(BaseModel):
    qr_code: str = Field(..., min_length=1, max_length=64)
    owner_name: Optional[str] = None
    owner_phone_e164: str = Field(..., min_length=3, max_length=32)


class CarRead(BaseModel):
    id: int
    qr_code: str
    owner_name: Optional[str]
    owner_phone_e164: str
    is_active: bool

    class Config:
        from_attributes = True


class IssueTypeCreate(BaseModel):
    code: str
    title: str
    description: Optional[str] = None


class IssueTypeRead(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class IssueReportCreate(BaseModel):
    issue_type_code: str
    comment: Optional[str] = None
    reporter_phone: Optional[str] = None


class IssueReportRead(BaseModel):
    id: int
    car_id: int
    issue_type_id: int
    comment: Optional[str]
    reporter_phone: Optional[str]

    class Config:
        from_attributes = True
