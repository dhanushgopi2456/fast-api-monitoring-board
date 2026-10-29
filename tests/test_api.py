import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import (
    get_health, get_users, get_products,
    simulate_error, simulate_timeout, simulate_rate_limit,
    auth_test_endpoint, get_prometheus_metrics,
    get_dashboard_summary, get_dashboard_timeseries,
    list_alerts, ack_alert, clear_alerts,
    run_simulation, get_recommendations, ask_ai,
    test_notification_channel as api_test_notification_channel,
    api_login, api_register
)
from app.models import (
    SimulationTrigger, AIQuestionRequest, NotificationTestRequest,
    LoginRequest, RegisterRequest
)
from app.database import init_db, seed_sample_history
from fastapi import HTTPException

def setup_module():
    init_db()
    seed_sample_history(force=True)

def test_health():
    h = get_health()
    assert h.status in ["Healthy", "Degraded", "Down"]
    assert h.uptime_seconds >= 0

def test_users():
    u = get_users()
    assert len(u) >= 5
    assert u[0]["name"]

def test_products():
    p = get_products()
    assert len(p) >= 5
    assert p[0]["sku"]

def test_simulate_error():
    with pytest.raises(HTTPException) as exc:
        simulate_error()
    assert exc.value.status_code == 500

def test_simulate_timeout():
    res = simulate_timeout(delay_seconds=0.01)
    assert res["status"] == "warning"

def test_simulate_rate_limit():
    with pytest.raises(HTTPException) as exc:
        simulate_rate_limit()
    assert exc.value.status_code == 429

def test_auth_endpoint():
    with pytest.raises(HTTPException) as exc:
        auth_test_endpoint(authorization=None)
    assert exc.value.status_code == 401
    
    valid = auth_test_endpoint(authorization="Bearer token123")
    assert valid["status"] == "authenticated"

def test_prometheus_metrics():
    prom = get_prometheus_metrics()
    assert "http_requests_total" in prom
    assert "api_uptime_ratio" in prom

def test_dashboard_summary():
    s = get_dashboard_summary()
    assert "uptime_percent" in s
    assert "avg_response_time_ms" in s
    assert "status_codes" in s

def test_simulations_and_rca():
    for sc in ["auth_failure", "timeout", "server_error", "rate_limit"]:
        res = run_simulation(SimulationTrigger(scenario_id=sc))
        assert "root_cause" in res
        assert "remediation" in res

def test_alerts_acknowledgement():
    alerts = list_alerts()
    assert len(alerts) > 0
    ack = ack_alert(alerts[0]["id"])
    assert ack["acknowledged"] is True

def test_ai_advisor():
    recs = get_recommendations()
    assert len(recs) > 0
    ans = ask_ai(AIQuestionRequest(question="Why did uptime drop?"))
    assert "answer" in ans

def test_notification_channels():
    res = api_test_notification_channel(NotificationTestRequest(channel="slack", custom_message="Unit test"))
    assert res["status"] == "success"

def test_login_and_register():
    reg = api_register(RegisterRequest(name="DevOps Lead", email="devops@novapulse.ai", password="secretpassword"))
    assert reg["status"] == "success"
    assert "token" in reg

    log = api_login(LoginRequest(email="devops@novapulse.ai", password="secretpassword"))
    assert log["status"] == "success"
    assert log["user"]["name"] == "DevOps Lead"
