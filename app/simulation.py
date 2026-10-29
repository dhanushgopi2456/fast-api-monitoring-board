import time
import datetime
from typing import Dict, Any, List
from app.database import log_simulation, get_db_connection
from app.alerts import evaluate_alert_rules

SIMULATION_SCENARIOS = {
    "auth_failure": {
        "id": "auth_failure",
        "name": "Invalid API Authentication",
        "endpoint": "/api/auth/test",
        "method": "GET",
        "expected_status": 401,
        "description": "Simulates an unauthenticated client request lacking a valid Bearer token.",
        "root_cause": "Authentication token missing or invalid: The request lacked required 'Authorization: Bearer <token>' header or token has expired. Verify API gateway credentials.",
        "remediation": "1. Ensure client includes Bearer token in headers.\n2. Verify JWT token expiry timestamp.\n3. Validate secret key and issuer in OAuth provider."
    },
    "timeout": {
        "id": "timeout",
        "name": "API Latency / Timeout (>3s)",
        "endpoint": "/simulate-timeout",
        "method": "GET",
        "expected_status": 200,
        "description": "Simulates upstream microservice latency delay exceeding the 3.0s SLA threshold.",
        "root_cause": "Upstream dependency delayed response: Upstream database / microservice spent 3,250ms processing query before returning. Breached 3000ms SLA threshold.",
        "remediation": "1. Add index on queried columns.\n2. Implement Redis caching layer with 60s TTL.\n3. Configure upstream circuit breaker with fallback."
    },
    "server_error": {
        "id": "server_error",
        "name": "Internal Server Error (HTTP 500)",
        "endpoint": "/simulate-error",
        "method": "GET",
        "expected_status": 500,
        "description": "Simulates an unhandled server-side exception during database transaction commit.",
        "root_cause": "Internal server error — check application logs: Database transaction deadlocked while executing batch write lock in worker thread.",
        "remediation": "1. Wrap critical section in defensive try-except block.\n2. Review lock acquisition ordering.\n3. Increase DB connection pool size from 10 to 30."
    },
    "rate_limit": {
        "id": "rate_limit",
        "name": "Rate Limit Exceeded (HTTP 429)",
        "endpoint": "/simulate-rate-limit",
        "method": "GET",
        "expected_status": 429,
        "description": "Simulates aggressive client request bursts depleting token bucket quota.",
        "root_cause": "Client exceeded allowed requests per minute: Token bucket algorithm depleted (limit: 60 req/min, burst: 10).",
        "remediation": "1. Client must implement exponential backoff with jitter.\n2. Upgrade API client to enterprise tier with higher throughput.\n3. Cache responses locally on client."
    }
}

def execute_simulation_scenario(scenario_id: str) -> Dict[str, Any]:
    """Execute a simulated failure scenario and return structured RCA."""
    if scenario_id not in SIMULATION_SCENARIOS:
        raise ValueError(f"Unknown scenario ID: {scenario_id}")

    scenario = SIMULATION_SCENARIOS[scenario_id]
    start_time = time.perf_counter()

    if scenario_id == "auth_failure":
        status_code = 401
        duration_ms = 24.5
        result_text = "Detected 401 Unauthorized"
    elif scenario_id == "timeout":
        # Simulate slight delay (e.g. 3.15s) or compute realistic simulated duration
        status_code = 200
        duration_ms = 3250.0 # >3000ms requirement
        result_text = "Detected high latency (>3000ms threshold breached)"
    elif scenario_id == "server_error":
        status_code = 500
        duration_ms = 65.2
        result_text = "Detected HTTP 500 Internal Server Error"
    elif scenario_id == "rate_limit":
        status_code = 429
        duration_ms = 18.0
        result_text = "Detected HTTP 429 Rate Limit Exceeded"
    else:
        status_code = 200
        duration_ms = 10.0
        result_text = "Success"

    # Evaluate alert rule
    evaluate_alert_rules(scenario["endpoint"], status_code, duration_ms, scenario["root_cause"])

    # Log to simulation history
    run_id = log_simulation(
        scenario_id=scenario["id"],
        scenario_name=scenario["name"],
        endpoint=scenario["endpoint"],
        status_code=status_code,
        duration_ms=duration_ms,
        result=result_text,
        root_cause=scenario["root_cause"]
    )

    return {
        "run_id": run_id,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scenario": scenario,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "result": result_text,
        "root_cause": scenario["root_cause"],
        "remediation": scenario["remediation"]
    }

def get_recent_simulations(limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM simulation_runs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
