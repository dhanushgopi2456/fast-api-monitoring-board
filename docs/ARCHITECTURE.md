# Monitoring Architecture & Data Flow

## Overview

The **PulseGuard FastAPI API Monitoring Board** is an end-to-end observability, alerting, and failure simulation system designed to monitor FastAPI REST applications with sub-millisecond precision.

```
+----------------------------------------------------------------------------------------+
|                                  INCOMING TRAFFIC / CLIENT                             |
+----------------------------------------------------------------------------------------+
                                           |
                                           v
+----------------------------------------------------------------------------------------+
|                          FastAPI Application (app.main:app)                            |
|                                                                                        |
|  [ ASGI Monitoring Middleware ]                                                        |
|     |---> High-resolution response latency tracking (time.perf_counter)                |
|     |---> Status code recording (2xx, 4xx, 5xx)                                        |
|     |---> Client IP & User Agent logging                                               |
|     |---> Threshold Evaluation Trigger                                                 |
|     |                                                                                  |
|     v                                                                                  |
|  [ REST API Endpoints ]       [ Observability API ]         [ AI SRE Advisor ]         |
|     - /health                    - /metrics (Prometheus)       - Gemini 1.5 Flash      |
|     - /users                     - /api/metrics/summary        - SRE Heuristic Engine  |
|     - /products                  - /api/metrics/timeseries     - Contextual Q&A        |
|     - /simulate-error            - /api/alerts                                         |
|     - /simulate-timeout          - /api/simulations/run                                |
|     - /simulate-rate-limit                                                             |
+----------------------------------------------------------------------------------------+
          |                                  |                           |
          v                                  v                           v
+-----------------------+          +-------------------+       +--------------------+
|  SQLite Database      |          | Prometheus / OTLP |       | Notification Hub   |
|  - request_logs       |          | Exporter          |       | - Slack Webhook    |
|  - alerts             |          | (Prometheus Scrape|       | - Email (SMTP)     |
|  - simulation_runs    |          |  Format)          |       | - Phone / SMS      |
+-----------------------+          +-------------------+       +--------------------+
```

## Key Components

1. **ASGI Monitoring Middleware (`app/monitoring.py`)**:
   - Intercepts 100% of incoming HTTP requests.
   - Computes execution duration in milliseconds.
   - Records request metadata to SQLite table `request_logs`.
   - Asynchronously triggers alert threshold evaluation on abnormal conditions.

2. **Metrics & Telemetry Engine (`app/monitoring.py`)**:
   - Computes rolling percentiles (p50, p95, p99) over rolling traffic windows.
   - Calculates availability ratio ($$ \text{Uptime} = 100\% - \frac{5\text{xx requests}}{\text{Total requests}} \times 100\% $$).
   - Generates Prometheus metrics in open metrics format (`/metrics`).

3. **Alert Rules Engine (`app/alerts.py`)**:
   - Evaluates:
     - Downtime & service health degradation.
     - Latency SLA breach (> 3,000ms threshold).
     - Internal server errors (HTTP 500).
     - Error rate spike (> 5.0% error ratio).
     - Client rate limit violations (HTTP 429).
   - Multi-channel notification dispatchers for Slack, Email, and SMS.

4. **Failure Simulation & RCA Engine (`app/simulation.py`)**:
   - Orchestrates 4 deterministic failure modes.
   - Emits structured Root Cause Analysis with diagnosis and recommended remediation.

5. **AI SRE Advisor (`app/ai_advisor.py`)**:
   - Dual-engine architecture:
     - Cloud Mode: Google Gemini API integration using contextual prompt templates.
     - Neural Heuristic Mode: Local rule-based expert telemetry analyzer with zero API key requirement.

