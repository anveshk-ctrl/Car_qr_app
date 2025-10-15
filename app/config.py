from __future__ import annotations

import os
from functools import lru_cache
from pydantic import BaseModel

# Load environment from .env if present
try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    pass


class Settings(BaseModel):
    # Default to SQLite local file
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./car_issues.db")

    twilio_account_sid: str | None = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token: str | None = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_from_number: str | None = os.getenv("TWILIO_FROM_NUMBER")

    # App
    app_name: str = os.getenv("APP_NAME", "Car Issue Reporting")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


@lru_cache
def get_settings() -> Settings:
    return Settings()
