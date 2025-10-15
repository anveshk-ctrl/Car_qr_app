# Car Issue Reporting Service

FastAPI service to collect car-issue reports via QR codes and notify owners by SMS.

## Features
- Public page to select an issue for a specific car (via QR code token)
- Records issue reports in SQL database
- Sends SMS to car owner (Twilio or console fallback)
- Simple admin endpoints to register cars and issue types

## Quickstart

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Open the public reporting page by scanning a QR that points to:

```
http://localhost:8000/report/<QR_CODE>
```

Example: `http://localhost:8000/report/ABC123`.

4. Register a car (so the QR_CODE resolves) via admin API:

```bash
curl -X POST http://localhost:8000/admin/cars \
  -H 'Content-Type: application/json' \
  -d '{"qr_code":"ABC123","owner_name":"Alice","owner_phone_e164":"+15551234567"}'
```

5. On first run, default issue types are seeded (e.g., WRONG_PARKING, BLOCKING, etc.). You can list them:

```bash
curl http://localhost:8000/admin/issue-types
```

## Environment Variables
Copy `.env.example` to `.env` and set values. For Twilio SMS:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER` (E.164 format)

If these are not set, messages are printed to stdout.

## Database
- Default is SQLite file at `car_issues.db` in project root. Configure via `DATABASE_URL`.

## QR Code
- Generate and print stickers with the unique `qr_code` string for each car. The URL encoded in the QR should be:
  `http://<your-domain>/report/<qr_code>`

## API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
