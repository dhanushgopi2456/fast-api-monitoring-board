import os
from pydantic import BaseModel

def _resolve_database_path() -> str:
    # On Vercel / serverless runtimes, the filesystem is read-only except /tmp
    if os.getenv("VERCEL") or os.getenv("VERCEL_ENV") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        return os.path.join("/tmp", "monitoring.db")
    return os.getenv("DATABASE_PATH", "monitoring.db")

class Settings(BaseModel):
    APP_NAME: str = "NovaPulse AI — FastAPI Observability Suite"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database (auto-adapts to /tmp on Vercel serverless)
    DATABASE_PATH: str = _resolve_database_path()
    
    # Alert Thresholds
    LATENCY_THRESHOLD_MS: float = float(os.getenv("LATENCY_THRESHOLD_MS", "3000.0")) # 3.0s requirement
    LATENCY_WARNING_MS: float = float(os.getenv("LATENCY_WARNING_MS", "1000.0"))
    ERROR_RATE_THRESHOLD_PERCENT: float = float(os.getenv("ERROR_RATE_THRESHOLD_PERCENT", "5.0")) # >5%
    
    # Rate Limiting Simulation Quota
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # LLM / AI Recommendations
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Notification Channels
    SLACK_WEBHOOK_URL: str = os.getenv("SLACK_WEBHOOK_URL", "")
    EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    EMAIL_SMTP_USER: str = os.getenv("EMAIL_SMTP_USER", "")
    EMAIL_SMTP_PASS: str = os.getenv("EMAIL_SMTP_PASS", "")
    EMAIL_ALERT_RECIPIENT: str = os.getenv("EMAIL_ALERT_RECIPIENT", "ops-team@example.com")
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_FROM: str = os.getenv("TWILIO_PHONE_FROM", "")
    TWILIO_PHONE_TO: str = os.getenv("TWILIO_PHONE_TO", "")

settings = Settings()
