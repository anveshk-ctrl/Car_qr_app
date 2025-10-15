from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .routers import public, admin
from .models import IssueType

app = FastAPI(title="Car Issue Reporting API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # Seed basic issue types if none exist
    from sqlalchemy.orm import Session

    with Session(bind=engine) as db:
        count = db.query(IssueType).count()
        if count == 0:
            db.add_all(
                [
                    IssueType(code="WRONG_PARKING", title="Parked at wrong place"),
                    IssueType(code="BLOCKING", title="Blocking driveway/entrance"),
                    IssueType(code="LIGHTS_ON", title="Lights left on"),
                    IssueType(code="ALARM", title="Car alarm ringing"),
                ]
            )
            db.commit()


app.include_router(public.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"status": "ok"}
