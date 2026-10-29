# Installation & Setup Guide

## System Prerequisites

- Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.13, 3.14)
- Pip package manager
- Modern Web Browser (Chrome, Firefox, Edge, Safari)

## Quick Start (Zero Config)

1. **Clone or Navigate to the Workspace**:
   ```bash
   cd fast-api-monitoring_board
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Application**:
   ```bash
   python run.py
   ```
   Or via Uvicorn directly:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Access the Monitoring Dashboard**:
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Environment Variables Configuration

The application works out of the box with default SQLite configuration, but supports environment variable overrides:

| Variable | Default | Purpose |
|---|---|---|
| `ENVIRONMENT` | `development` | Deployment environment name |
| `DATABASE_PATH` | `monitoring.db` | Path to SQLite database file |
| `LATENCY_THRESHOLD_MS` | `3000.0` | High latency alert threshold (ms) |
| `ERROR_RATE_THRESHOLD_PERCENT` | `5.0` | Error percentage threshold (%) |
| `GEMINI_API_KEY` | `""` | Optional Google Gemini API key for live AI recommendations |
| `SLACK_WEBHOOK_URL` | `""` | Incoming Slack Webhook URL |
| `EMAIL_SMTP_HOST` | `""` | Outgoing SMTP mail server |
| `EMAIL_SMTP_USER` | `""` | SMTP authentication user |
| `EMAIL_SMTP_PASS` | `""` | SMTP authentication password |
| `EMAIL_ALERT_RECIPIENT`| `ops-team@example.com` | Alert destination email address |
| `TWILIO_ACCOUNT_SID` | `""` | Twilio Account SID for phone/SMS alerts |
| `TWILIO_AUTH_TOKEN` | `""` | Twilio Auth Token |

---

## Running the Automated Test Suite

Run the full pytest suite:
```bash
python -m pytest tests/test_api.py -v
```

Run the unittesting verification script:
```bash
python tests/verify_all.py
```

