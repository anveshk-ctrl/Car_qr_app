from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .db import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String(64), unique=True, index=True, nullable=False)  # string printed on QR
    owner_name = Column(String(120), nullable=True)
    owner_phone_e164 = Column(String(32), nullable=False)  # e.g. +15551234567
    is_active = Column(Boolean, default=True, nullable=False)

    reports = relationship("IssueReport", back_populates="car")


class IssueType(Base):
    __tablename__ = "issue_types"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False)  # e.g. WRONG_PARKING
    title = Column(String(120), nullable=False)  # e.g. Parked at wrong place
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    reports = relationship("IssueReport", back_populates="issue_type")


class IssueReport(Base):
    __tablename__ = "issue_reports"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    issue_type_id = Column(Integer, ForeignKey("issue_types.id"), nullable=False)
    comment = Column(Text, nullable=True)
    reporter_phone = Column(String(32), nullable=True)
    reporter_ip = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    car = relationship("Car", back_populates="reports")
    issue_type = relationship("IssueType", back_populates="reports")

    __table_args__ = (
        UniqueConstraint("id", name="uq_issue_report_id"),
    )
