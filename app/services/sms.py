from __future__ import annotations

from typing import Optional
from ..config import get_settings


class SmsSender:
    def __init__(self) -> None:
        settings = get_settings()
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.from_number = settings.twilio_from_number

        self._client = None
        if self.account_sid and self.auth_token and self.from_number:
            try:
                from twilio.rest import Client  # type: ignore

                self._client = Client(self.account_sid, self.auth_token)
            except Exception:
                self._client = None

    def send(self, to_e164: str, body: str) -> None:
        if self._client and self.from_number:
            self._client.messages.create(to=to_e164, from_=self.from_number, body=body)
        else:
            # Fallback: log to stdout
            print(f"[SMS FALLBACK] to={to_e164} body={body}")


sms_sender = SmsSender()
