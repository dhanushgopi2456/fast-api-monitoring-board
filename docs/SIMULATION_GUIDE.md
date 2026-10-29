# Failure Simulation & Chaos Testing Guide

This guide describes how to trigger and verify each of the 4 failure scenarios from both the Dashboard UI and the CLI.

---

## Scenario Matrix

| Scenario | Trigger Endpoint | Detection Metric | Alert Generated | Root Cause Output |
|---|---|---|---|---|
| **1. Invalid Auth** | `/api/auth/test` | HTTP 401 | `Unauthorized Access Attempt` | "Authentication token missing or invalid: The request lacked required 'Authorization: Bearer <token>' header or token has expired. Verify API gateway credentials." |
| **2. API Timeout** | `/simulate-timeout` | Duration &gt; 3,000ms | `High Latency Threshold (>3s)` | "Upstream dependency delayed response: Upstream database / microservice spent 3,250ms processing query before returning. Breached 3000ms SLA threshold." |
| **3. Server Error** | `/simulate-error` | HTTP 500 | `HTTP 500 Internal Server Error` | "Internal server error — check application logs: Database transaction deadlocked while executing batch write lock in worker thread." |
| **4. Rate Limit** | `/simulate-rate-limit` | HTTP 429 | `Rate Limit Exceeded (HTTP 429)` | "Client exceeded allowed requests per minute: Token bucket algorithm depleted (limit: 60 req/min, burst: 10)." |

---

## Triggering via Dashboard UI

1. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
2. Navigate to the **Failure Sandbox** tab (or use the quick trigger buttons on the Overview page).
3. Click any of the 4 simulation buttons:
   - **Trigger 401 Auth Failure**
   - **Trigger >3s Timeout Delay**
   - **Trigger 500 Server Crash**
   - **Trigger 429 Rate Limit**
4. Observe the synchronized system response:
   - Audio tone plays (tone pitch matches severity).
   - Animated pop-up toast notification appears with status code and duration.
   - An alert record is created in the **Alerts Center**.
   - Root Cause Analysis modal opens with diagnosis and remediation runbook.
   - Executive metrics (Availability %, Error Rate, Latency) update in real-time.

---

## Triggering via REST API (cURL)

```bash
# 1. Invalid Authentication (401)
curl -i http://127.0.0.1:8000/api/auth/test

# 2. Latency / Timeout (>3s)
curl -i http://127.0.0.1:8000/simulate-timeout

# 3. Server Error (500)
curl -i http://127.0.0.1:8000/simulate-error

# 4. Rate Limit (429)
curl -i http://127.0.0.1:8000/simulate-rate-limit

# Trigger via Simulation Orchestrator
curl -X POST http://127.0.0.1:8000/api/simulations/run \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "server_error"}'
```

