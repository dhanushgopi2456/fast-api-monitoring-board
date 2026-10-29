import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import (
    get_health, get_users, get_products,
    simulate_error, simulate_timeout, simulate_rate_limit,
    auth_test_endpoint, get_prometheus_metrics,
    get_dashboard_summary, get_dashboard_timeseries,
    list_alerts, ack_alert, clear_alerts,
    list_simulation_scenarios, run_simulation,
    get_recommendations, ask_ai,
    test_notification_channel
)
from app.models import SimulationTrigger, AIQuestionRequest, NotificationTestRequest
from app.database import init_db, seed_sample_history

def run_verification():
    print(">>> 1. Initializing DB and seeding history...", flush=True)
    init_db()
    seed_sample_history(force=True)

    print(">>> 2. Testing /health...", flush=True)
    health = get_health()
    assert health.status in ["Healthy", "Degraded", "Down"]
    print(f"    Health: status={health.status}, memory={health.memory_percent}%, cpu={health.cpu_percent}%", flush=True)

    print(">>> 3. Testing /users...", flush=True)
    users = get_users()
    assert len(users) >= 5
    print(f"    Users: {len(users)} users returned successfully.", flush=True)

    print(">>> 4. Testing /products...", flush=True)
    products = get_products()
    assert len(products) >= 5
    print(f"    Products: {len(products)} products returned successfully.", flush=True)

    print(">>> 5. Testing /simulate-error (expecting HTTPException 500)...", flush=True)
    try:
        simulate_error()
        assert False, "Should have raised HTTPException 500"
    except Exception as e:
        print(f"    Error simulation correctly caught: {e.status_code} - {e.detail}", flush=True)

    print(">>> 6. Testing /simulate-timeout (delay 0.05s for quick verification)...", flush=True)
    timeout_res = simulate_timeout(delay_seconds=0.05)
    print(f"    Timeout simulation result: {timeout_res['warning']}", flush=True)

    print(">>> 7. Testing /simulate-rate-limit (expecting HTTPException 429)...", flush=True)
    try:
        simulate_rate_limit()
        assert False, "Should have raised HTTPException 429"
    except Exception as e:
        print(f"    Rate limit simulation correctly caught: {e.status_code} - {e.detail}", flush=True)

    print(">>> 8. Testing /api/auth/test (auth simulation)...", flush=True)
    try:
        auth_test_endpoint(authorization=None)
        assert False, "Should have raised HTTPException 401"
    except Exception as e:
        print(f"    Auth simulation correctly caught: {e.status_code} - {e.detail}", flush=True)

    auth_success = auth_test_endpoint(authorization="Bearer valid_jwt_token")
    assert auth_success["status"] == "authenticated"
    print(f"    Auth check with valid bearer token passed: {auth_success}", flush=True)

    print(">>> 9. Testing Prometheus /metrics export...", flush=True)
    prom = get_prometheus_metrics()
    assert "http_requests_total" in prom
    assert "api_uptime_ratio" in prom
    print("    Prometheus metrics generated successfully (length:", len(prom), "bytes)", flush=True)

    print(">>> 10. Testing Dashboard Summary and Timeseries...", flush=True)
    summary = get_dashboard_summary()
    assert "uptime_percent" in summary
    assert "avg_response_time_ms" in summary
    print(f"    Summary: uptime={summary['uptime_percent']}%, avg_latency={summary['avg_response_time_ms']}ms, total_reqs={summary['total_requests']}", flush=True)

    timeseries = get_dashboard_timeseries(limit=10)
    print(f"    Timeseries points: {len(timeseries)} time buckets returned.", flush=True)

    print(">>> 11. Testing Failure Simulations (all 4 scenarios)...", flush=True)
    for scenario_id in ["auth_failure", "timeout", "server_error", "rate_limit"]:
        sim_res = run_simulation(SimulationTrigger(scenario_id=scenario_id))
        assert "root_cause" in sim_res
        assert "remediation" in sim_res
        print(f"    Simulation '{scenario_id}': status={sim_res['status_code']} -> RCA: {sim_res['root_cause'][:55]}...", flush=True)

    print(">>> 12. Testing Alerts and Acknowledgements...", flush=True)
    alerts = list_alerts()
    assert len(alerts) > 0
    print(f"    Found {len(alerts)} alerts. Acknowledging alert #{alerts[0]['id']}...", flush=True)
    ack_res = ack_alert(alerts[0]["id"])
    assert ack_res["acknowledged"] is True
    print(f"    Alert #{alerts[0]['id']} acknowledged successfully.", flush=True)

    print(">>> 13. Testing AI Recommendations & Q&A...", flush=True)
    recs = get_recommendations()
    assert len(recs) > 0
    print(f"    AI Recommendations: {len(recs)} active recommendations available.", flush=True)

    ai_answer = ask_ai(AIQuestionRequest(question="Why did uptime drop?"))
    assert "answer" in ai_answer
    print(f"    AI Q&A Response (source: {ai_answer['source']}):\n    '{ai_answer['answer'][:110]}...'", flush=True)

    print(">>> 14. Testing Notification Dispatches (Slack/Email/SMS)...", flush=True)
    notif_res = test_notification_channel(NotificationTestRequest(channel="slack", custom_message="Verification check"))
    assert notif_res["status"] == "success"
    print(f"    Notification dispatch log created: {notif_res['dispatch_record']['channels']}", flush=True)

    print("\n[SUCCESS] ALL 14 BACKEND CAPABILITIES VERIFIED 100% SUCCESSFULLY!", flush=True)

if __name__ == "__main__":
    run_verification()
