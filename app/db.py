from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import get_settings

settings = get_settings()

# sqlite URL handling
if settings.database_url.startswith("sqlite"):  # allow sqlite in file
    engine = create_engine(settings.database_url.replace("sqlite+sqlite", "sqlite"), connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
