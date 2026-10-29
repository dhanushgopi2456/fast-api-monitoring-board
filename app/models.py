from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class User(BaseModel):
    id: int
    name: str
    email: str
    role: str
    status: str
    department: str
    avatar_url: str

class Product(BaseModel):
    id: int
    sku: str
    name: str
    category: str
    price: float
    stock: int
    rating: float

class HealthStatus(BaseModel):
    status: str
    timestamp: str
    uptime_seconds: float
    version: str
    database: str
    memory_percent: float
    cpu_percent: float
    active_alerts: int

class SimulationTrigger(BaseModel):
    scenario_id: str = Field(..., description="auth_failure | timeout | server_error | rate_limit")

class AIQuestionRequest(BaseModel):
    question: str

class NotificationTestRequest(BaseModel):
    channel: str = Field(..., description="email | slack | twilio_sms")
    custom_message: Optional[str] = "NovaPulse AI API Alert Verification Ping"

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "Lead Site Reliability Engineer"
    department: Optional[str] = "Platform Operations"
