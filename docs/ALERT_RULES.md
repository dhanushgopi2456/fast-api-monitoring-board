# Alert Rules, Thresholds & Notification Channels

## 1. Alert Rule Catalog

| Rule Name | Severity | Condition | Root Cause Diagnosis | Remediation Action |
|---|---|---|---|---|
| **API Downtime** | `CRITICAL` | Service health status is `Down` or `/health` fails | Application worker crash or database lock | Restart worker threads, verify SQLite disk permissions |
| **High Latency SLA Breach** | `WARNING` | Duration &gt; `3,000ms` | Upstream database or external dependency latency | Implement Redis caching, optimize queries, add client timeout |
| **HTTP 500 Server Error** | `CRITICAL` | Status Code &gt;= `500` | Unhandled exception during transaction | Wrap handler in try-except, inspect application stack traces |
| **High Failure Rate Spike** | `WARNING` | Error Percentage &gt; `5.0%` | Surge in 4xx client or 5xx server errors | Investigate top failing endpoints, audit client credentials |
| **Rate Limit Exceeded** | `WARNING` | Status Code == `429` | Client exceeded 60 requests/minute quota | Client must implement exponential backoff with jitter |
| **Unauthorized Access Attempt** | `WARNING` | Status Code == `401` | Missing or expired Bearer authorization token | Ensure client includes valid JWT in Authorization header |

---

## 2. Notification Channels

### A. Slack Incoming Webhooks
- **Trigger**: Dispatches color-coded attachment card (`#ef4444` for Critical, `#f59e0b` for Warning).
- **Setup**:
  ```bash
  export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T000/B000/XXXX"
  ```
- **Payload Example**:
  ```json
  {
    "attachments": [
      {
        "color": "#ef4444",
        "title": "🚨 [CRITICAL] HTTP 500 Internal Server Error",
        "text": "*Endpoint: /simulate-error*\nServer returned HTTP 500 on /simulate-error\n_Time: 2026-10-27 17:30:00_",
        "footer": "Antigravity API Monitor"
      }
    ]
  }
  ```

### B. Email (SMTP / SendGrid / Resend)
- **Setup**:
  ```bash
  export EMAIL_SMTP_HOST="smtp.sendgrid.net"
  export EMAIL_SMTP_PORT=587
  export EMAIL_SMTP_USER="apikey"
  export EMAIL_SMTP_PASS="YOUR_SENDGRID_KEY"
  export EMAIL_ALERT_RECIPIENT="sre-team@yourcompany.com"
  ```

### C. Phone / SMS (Twilio)
- **Setup**:
  ```bash
  export TWILIO_ACCOUNT_SID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  export TWILIO_AUTH_TOKEN="your_auth_token"
  export TWILIO_PHONE_FROM="+1234567890"
  export TWILIO_PHONE_TO="+1987654321"
  ```

