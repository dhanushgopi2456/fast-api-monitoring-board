import asyncio
import os
import time
import datetime
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Header, Depends, Query
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, seed_sample_history, get_db_connection
from app.monitoring import (
    MonitoringMiddleware,
    get_metrics_summary,
    get_timeseries_metrics,
    generate_prometheus_metrics,
    get_system_stats
)
from app.alerts import (
    get_alerts,
    acknowledge_alert,
    clear_all_alerts,
    dispatch_notifications,
    NOTIFICATION_DISPATCH_LOG
)
from app.simulation import (
    execute_simulation_scenario,
    get_recent_simulations,
    SIMULATION_SCENARIOS
)
from app.ai_advisor import (
    generate_ai_recommendations,
    ask_ai_question,
    update_recommendation_status
)
from app.models import (
    User, Product, HealthStatus, SimulationTrigger,
    AIQuestionRequest, NotificationTestRequest,
    LoginRequest, RegisterRequest
)

# Startup and shutdown lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and seed initial data
    init_db()
    seed_sample_history()
    print("[+] NovaPulse AI FastAPI Monitoring Board initialized successfully.")
    yield
    print("[-] NovaPulse AI FastAPI Monitoring Board shutting down.")

# Auto-initialize DB on import for serverless environments (Vercel)
try:
    init_db()
    seed_sample_history()
except Exception as _e:
    pass

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready FastAPI API Monitoring & Observability Board",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Monitoring Middleware (tracks response times, status codes, logs, and triggers alerts)
# app.add_middleware(MonitoringMiddleware)

# Sample Users Dataset
SAMPLE_USERS = [
    {
        "id": 1,
        "name": "Alex Mercer",
        "email": "alex.mercer@novapulse.ai",
        "role": "Lead Site Reliability Engineer",
        "status": "Active",
        "department": "Platform Operations",
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80"
    },
    {
        "id": 2,
        "name": "Elena Rostova",
        "email": "elena.rostova@novapulse.ai",
        "role": "Principal Backend Architect",
        "status": "Active",
        "department": "Core Engine",
        "avatar_url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100&auto=format&fit=crop&q=80"
    },
    {
        "id": 3,
        "name": "Marcus Vance",
        "email": "marcus.vance@novapulse.ai",
        "role": "DevOps Automation Specialist",
        "status": "Active",
        "department": "Infrastructure",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80"
    },
    {
        "id": 4,
        "name": "Samantha Chen",
        "email": "samantha.chen@novapulse.ai",
        "role": "Security & Compliance Auditor",
        "status": "Active",
        "department": "InfoSec",
        "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&auto=format&fit=crop&q=80"
    },
    {
        "id": 5,
        "name": "David Kim",
        "email": "david.kim@novapulse.ai",
        "role": "Distributed Systems Engineer",
        "status": "On-Call",
        "department": "Core Engine",
        "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80"
    }
]

# Sample Products Dataset
SAMPLE_PRODUCTS = [
    {
        "id": 101,
        "sku": "SRV-H100-NODE",
        "name": "NVIDIA H100 GPU Inference Cluster",
        "category": "Compute Hardware",
        "price": 32999.00,
        "stock": 14,
        "rating": 4.95
    },
    {
        "id": 102,
        "sku": "DB-VEC-ULTRA",
        "name": "NovaPulse Spatial Vector Database",
        "category": "Cloud Services",
        "price": 1250.00,
        "stock": 250,
        "rating": 4.88
    },
    {
        "id": 103,
        "sku": "NET-EDGE-W3",
        "name": "Global Anycast Edge Accelerator",
        "category": "Networking",
        "price": 450.00,
        "stock": 1200,
        "rating": 4.92
    },
    {
        "id": 104,
        "sku": "MEM-REDIS-X8",
        "name": "Fault-Tolerant Distributed Memory Cache",
        "category": "Storage",
        "price": 680.00,
        "stock": 85,
        "rating": 4.81
    },
    {
        "id": 105,
        "sku": "SEC-WAF-GEN2",
        "name": "AI-Powered Autonomous Web Firewall",
        "category": "Security",
        "price": 890.00,
        "stock": 500,
        "rating": 4.97
    }
]

# =========================================================================
# REQUIRED SAMPLE REST ENDPOINTS
# =========================================================================

@app.get("/health", response_model=HealthStatus, tags=["Core API"])
def get_health():
    """Returns API health status (healthy/degraded/unhealthy) with vital telemetry."""
    summary = get_metrics_summary()
    sys_stats = summary["system_stats"]
    
    return HealthStatus(
        status=summary["service_status"],
        timestamp=datetime.datetime.now().isoformat(),
        uptime_seconds=sys_stats["uptime_seconds"],
        version=settings.APP_VERSION,
        database="SQLite (WAL mode active)",
        memory_percent=sys_stats["memory_percent"],
        cpu_percent=sys_stats["cpu_percent"],
        active_alerts=summary["active_alerts_count"]
    )

@app.get("/users", response_model=List[User], tags=["Core API"])
def get_users():
    """Returns sample user data (JSON list)."""
    return SAMPLE_USERS

@app.get("/products", response_model=List[Product], tags=["Core API"])
def get_products():
    """Returns sample product data (JSON list)."""
    return SAMPLE_PRODUCTS

@app.get("/simulate-error", tags=["Failure Simulation"])
def simulate_error():
    """Generates an intentional server error response (HTTP 500)."""
    raise HTTPException(
        status_code=500,
        detail="Internal server error: Database transaction deadlocked while executing batch write lock in worker thread."
    )

@app.get("/simulate-timeout", tags=["Failure Simulation"])
def simulate_timeout(delay_seconds: float = 3.2):
    """Simulates a delayed API response (>3s timeout scenario)."""
    if delay_seconds > 0:
        time.sleep(delay_seconds)
    return {
        "status": "warning",
        "message": f"Delayed response executed after {delay_seconds}s.",
        "warning": "Duration exceeded 3.0s SLA threshold. High latency alert recorded.",
        "threshold_seconds": 3.0,
        "actual_seconds": delay_seconds
    }

@app.get("/simulate-rate-limit", tags=["Failure Simulation"])
def simulate_rate_limit():
    """Simulates a rate limit failure (HTTP 429)."""
    raise HTTPException(
        status_code=429,
        detail="Rate limit exceeded: 60 requests per minute quota reached. Retry-After: 60"
    )

@app.get("/api/auth/test", tags=["Failure Simulation"])
def auth_test_endpoint(authorization: Optional[str] = Header(None)):
    """Simulates authentication check; returns 401 Unauthorized if Bearer token is missing."""
    if not authorization or not authorization.startswith("Bearer ") or authorization == "Bearer invalid":
        raise HTTPException(
            status_code=401,
            detail="Authentication token missing or invalid: The request lacked required 'Authorization: Bearer <token>' header or token has expired. Verify API gateway credentials."
        )
    return {
        "status": "authenticated",
        "message": "Token verification passed.",
        "principal": "service-worker-01"
    }

@app.post("/api/auth/login", tags=["Authentication"])
def api_login(req: LoginRequest):
    """Authenticates operator credentials and returns session token."""
    for user in SAMPLE_USERS:
        if user["email"].lower() == req.email.strip().lower():
            return {
                "status": "success",
                "token": f"np_sec_token_{user['id']}_{int(time.time())}",
                "user": user,
                "message": f"Welcome back, {user['name']}!"
            }
    if "@" in req.email:
        name_part = req.email.split("@")[0].replace(".", " ").title()
        user_data = {
            "id": len(SAMPLE_USERS) + 1,
            "name": name_part,
            "email": req.email.strip(),
            "role": "Lead Site Reliability Engineer",
            "status": "Active",
            "department": "Platform Operations",
            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80"
        }
        return {
            "status": "success",
            "token": f"np_sec_token_custom_{int(time.time())}",
            "user": user_data,
            "message": f"Welcome back, {user_data['name']}!"
        }
    raise HTTPException(status_code=400, detail="Invalid email format.")

@app.post("/api/auth/register", tags=["Authentication"])
def api_register(req: RegisterRequest):
    """Registers a new SRE / DevOps operator."""
    new_user = {
        "id": len(SAMPLE_USERS) + 1,
        "name": req.name.strip(),
        "email": req.email.strip(),
        "role": req.role or "Site Reliability Engineer",
        "status": "Active",
        "department": req.department or "Platform Operations",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80"
    }
    SAMPLE_USERS.append(new_user)
    return {
        "status": "success",
        "token": f"np_sec_token_{new_user['id']}_{int(time.time())}",
        "user": new_user,
        "message": f"Welcome to NovaPulse AI, {new_user['name']}!"
    }

@app.get("/metrics", response_class=PlainTextResponse, tags=["Monitoring"])
def get_prometheus_metrics():
    """Exposes real-time metrics in Prometheus exposition format."""
    return generate_prometheus_metrics()

@app.get("/api/metrics/summary", tags=["Monitoring"])
def get_dashboard_summary():
    """Returns aggregated executive metrics for the frontend dashboard."""
    return get_metrics_summary()

@app.get("/api/metrics/timeseries", tags=["Monitoring"])
def get_dashboard_timeseries(limit: int = Query(30, ge=5, le=100)):
    """Returns historical time-series data points for charts."""
    return get_timeseries_metrics(limit=limit)

@app.get("/api/logs", tags=["Monitoring"])
def get_recent_logs(limit: int = Query(25, ge=5, le=100)):
    """Returns recent raw request logs from SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM request_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/alerts", tags=["Alerts"])
def list_alerts(status: Optional[str] = None):
    """Retrieve all alert records or filter by status (active / acknowledged)."""
    return get_alerts(status_filter=status)

@app.post("/api/alerts/{alert_id}/ack", tags=["Alerts"])
def ack_alert(alert_id: int):
    """Acknowledge an alert."""
    success = acknowledge_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert ID not found")
    return {"status": "success", "alert_id": alert_id, "acknowledged": True}

@app.post("/api/alerts/clear", tags=["Alerts"])
def clear_alerts():
    """Clear all alert records from the database."""
    cleared = clear_all_alerts()
    return {"status": "success", "cleared_count": cleared}

@app.post("/api/notifications/test", tags=["Alerts"])
def test_notification_channel(payload: NotificationTestRequest):
    """Test notification dispatching across Email, Slack, or Twilio."""
    result = dispatch_notifications(
        severity="INFO",
        title="NovaPulse AI Test Verification",
        endpoint="/api/notifications/test",
        details=f"Manual channel test for '{payload.channel}': {payload.custom_message}"
    )
    return {"status": "success", "dispatch_record": result}

@app.get("/api/notifications/history", tags=["Alerts"])
def get_notification_history():
    """Returns audit log of all notification dispatches."""
    return NOTIFICATION_DISPATCH_LOG

@app.get("/api/simulations/scenarios", tags=["Simulation"])
def list_simulation_scenarios():
    """List available failure simulation scenarios."""
    return list(SIMULATION_SCENARIOS.values())

@app.post("/api/simulations/run", tags=["Simulation"])
def run_simulation(trigger: SimulationTrigger):
    """Trigger a failure simulation and return instant Root Cause Analysis."""
    try:
        result = execute_simulation_scenario(trigger.scenario_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/simulations/history", tags=["Simulation"])
def simulation_history(limit: int = 10):
    """Retrieve history of executed simulation runs."""
    return get_recent_simulations(limit=limit)

@app.get("/api/ai/recommendations", tags=["AI Advisor"])
def get_recommendations():
    """Retrieve AI-powered recommendations for performance and reliability."""
    return generate_ai_recommendations()

@app.post("/api/ai/recommendations/{rec_id}/action", tags=["AI Advisor"])
def handle_recommendation_action(rec_id: str, action: str = Query(..., pattern="^(accepted|dismissed)$")):
    """Accept or dismiss an AI recommendation."""
    success = update_recommendation_status(rec_id, action)
    return {"status": "success", "rec_id": rec_id, "action": action, "updated": success}

@app.post("/api/ai/ask", tags=["AI Advisor"])
def ask_ai(req: AIQuestionRequest):
    """Ask a free-form question to the NovaPulse AI SRE Advisor."""
    return ask_ai_question(req.question)

# =========================================================================
# STATIC FILES MOUNT & ROOT DASHBOARD
# =========================================================================

static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Serves the main NovaPulse AI Monitoring Dashboard UI."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
        "metrics": "/metrics"
    }
