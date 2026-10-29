import datetime
import smtplib
import json
import httpx
from typing import List, Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.database import get_db_connection, create_alert
from app.config import settings

# In-memory log of notification dispatches for audit and UI proof
NOTIFICATION_DISPATCH_LOG: List[Dict[str, Any]] = []

def evaluate_alert_rules(endpoint: str, status_code: int, duration_ms: float, error_message: Optional[str] = None):
    """Evaluates incoming request telemetry against configured alert thresholds."""
    
    # 1. HTTP 500 Server Error
    if status_code >= 500:
        alert_id = create_alert(
            rule_name="HTTP 500 Internal Server Error",
            severity="CRITICAL",
            endpoint=endpoint,
            message=f"Server returned HTTP {status_code} on {endpoint}.",
            root_cause="Internal server error in request handler execution. Check application stack trace.",
            remediation="Inspect server logs, verify database connection availability, and validate transaction bounds."
        )
        dispatch_notifications("CRITICAL", "HTTP 500 Internal Server Error", endpoint, f"HTTP {status_code} detected on {endpoint}")

    # 2. Response Time > 3 Seconds (3000ms)
    elif duration_ms > settings.LATENCY_THRESHOLD_MS:
        alert_id = create_alert(
            rule_name="High Latency Threshold (>3s)",
            severity="WARNING",
            endpoint=endpoint,
            message=f"Response time spiked to {duration_ms}ms (threshold: {settings.LATENCY_THRESHOLD_MS}ms).",
            root_cause="Upstream dependency latency or unoptimized blocking I/O call.",
            remediation="Profile endpoint database queries, introduce asynchronous I/O, and configure caching."
        )
        dispatch_notifications("WARNING", "High Latency Threshold (>3s)", endpoint, f"Duration: {duration_ms}ms on {endpoint}")

    # 3. Rate Limit Exceeded (HTTP 429)
    elif status_code == 429:
        alert_id = create_alert(
            rule_name="Rate Limit Exceeded (HTTP 429)",
            severity="WARNING",
            endpoint=endpoint,
            message=f"Client triggered HTTP 429 Too Many Requests on {endpoint}.",
            root_cause="Client exceeded allowed request quota per minute threshold.",
            remediation="Implement client-side exponential backoff, request batching, or request rate quota increase."
        )
        dispatch_notifications("WARNING", "Rate Limit Exceeded", endpoint, f"Rate limit reached on {endpoint}")

    # 4. Authentication Failure (HTTP 401)
    elif status_code == 401:
        alert_id = create_alert(
            rule_name="Unauthorized Access Attempt (HTTP 401)",
            severity="WARNING",
            endpoint=endpoint,
            message=f"Unauthorized request on protected endpoint {endpoint}.",
            root_cause="Authentication token missing, expired, or signature verification failed.",
            remediation="Check client API key / Bearer authorization headers and token expiration."
        )
        dispatch_notifications("WARNING", "Unauthorized Access", endpoint, f"Auth failed on {endpoint}")

def dispatch_notifications(severity: str, title: str, endpoint: str, details: str) -> Dict[str, Any]:
    """Dispatches notifications across Email, Slack, and Twilio channels."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    dispatch_record = {
        "id": len(NOTIFICATION_DISPATCH_LOG) + 1,
        "timestamp": timestamp,
        "severity": severity,
        "title": title,
        "endpoint": endpoint,
        "details": details,
        "channels": {}
    }

    # 1. Slack Webhook Dispatch
    slack_status = "simulated"
    if settings.SLACK_WEBHOOK_URL:
        try:
            color = "#ef4444" if severity == "CRITICAL" else "#f59e0b"
            payload = {
                "attachments": [
                    {
                        "color": color,
                        "title": f"🚨 [{severity}] {title}",
                        "text": f"*{endpoint}*\n{details}\n_Time: {timestamp}_",
                        "footer": "NovaPulse AI API Monitor"
                    }
                ]
            }
            httpx.post(settings.SLACK_WEBHOOK_URL, json=payload, timeout=5.0)
            slack_status = "sent"
        except Exception as e:
            slack_status = f"failed: {str(e)}"
    else:
        slack_status = "simulated_success (Configure SLACK_WEBHOOK_URL for live delivery)"
    dispatch_record["channels"]["slack"] = slack_status

    # 2. Email Dispatch
    email_status = "simulated"
    if settings.EMAIL_SMTP_HOST and settings.EMAIL_SMTP_USER:
        try:
            msg = MIMEMultipart()
            msg["From"] = settings.EMAIL_SMTP_USER
            msg["To"] = settings.EMAIL_ALERT_RECIPIENT
            msg["Subject"] = f"[{severity} ALERT] {title} on {endpoint}"
            body = f"Alert Triggered:\nSeverity: {severity}\nTitle: {title}\nEndpoint: {endpoint}\nDetails: {details}\nTimestamp: {timestamp}"
            msg.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_SMTP_USER, settings.EMAIL_SMTP_PASS)
                server.send_message(msg)
            email_status = "sent"
        except Exception as e:
            email_status = f"failed: {str(e)}"
    else:
        email_status = f"simulated_success (Queued for {settings.EMAIL_ALERT_RECIPIENT})"
    dispatch_record["channels"]["email"] = email_status

    # 3. Twilio / SMS Dispatch
    twilio_status = "simulated"
    if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
        try:
            # Twilio REST API SMS endpoint
            url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
            data = {
                "From": settings.TWILIO_PHONE_FROM,
                "To": settings.TWILIO_PHONE_TO,
                "Body": f"[{severity}] {title}: {endpoint} - {details}"
            }
            httpx.post(url, data=data, auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN), timeout=5.0)
            twilio_status = "sent"
        except Exception as e:
            twilio_status = f"failed: {str(e)}"
    else:
        twilio_status = "simulated_success (Mock SMS dispatched to on-call ops engineer)"
    dispatch_record["channels"]["twilio_sms"] = twilio_status

    NOTIFICATION_DISPATCH_LOG.insert(0, dispatch_record)
    if len(NOTIFICATION_DISPATCH_LOG) > 50:
        NOTIFICATION_DISPATCH_LOG.pop()

    return dispatch_record

def get_alerts(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if status_filter:
        cursor.execute("SELECT * FROM alerts WHERE status = ? ORDER BY id DESC LIMIT 50", (status_filter,))
    else:
        cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 50")
        
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(r) for r in rows]

def acknowledge_alert(alert_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE alerts SET status = 'acknowledged', acknowledged_at = ? WHERE id = ?", (now_iso, alert_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def clear_all_alerts() -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count
