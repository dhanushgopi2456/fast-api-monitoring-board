# 🚀 NovaPulse AI — FastAPI API Monitoring & Observability Dashboard

A production-ready, full-stack API monitoring, incident alerting, and chaos failure simulation platform for FastAPI applications. Built with **FastAPI**, **SQLite**, **Tailwind CSS**, **HTML5 Web Audio API**, **Chart.js**, and **Google Gemini AI**.

---

## 🌟 Key Capabilities

- **Real-Time Telemetry Tracking**: Nanosecond request logging, latency percentiles (average, p95, p99), availability ratio, status code breakdown (2xx, 4xx, 5xx), and requests per minute (RPM).
- **HD Animated Graphics**: Interactive 2D/3D particle mesh canvas, glowing status beacons, animated SVG ECG heartbeat vital line, orbital loading scanners, and floating satellite empty states.
- **Synthesized Audio Feedback**: Pure HTML5 Web Audio API synthesizer with zero external file dependencies. Contextual tones for clicks, navigation, successes, warnings, destructive actions, and failure simulation triggers.
- **Chaos Failure Simulation**: One-click simulation of 4 critical API failure scenarios with automated Root Cause Analysis (RCA) output and remediation playbooks.
- **Multi-Channel Alert Center**: Configured alert rules for downtime, >3s latency, HTTP 500 crashes, and >5% error rate spikes, with dispatchers for Slack Webhooks, Email (SMTP), and Phone/SMS (Twilio).
- **AI SRE Advisor**: Google Gemini 1.5 Flash integration with fallback to built-in SRE telemetry heuristics for instant diagnostics and free-form natural language Q&A.
- **Glassmorphism Dark & Light Theme**: Deep space obsidian dark mode and clean frosted slate light mode with persistent `localStorage` preference.

---

## 🏗️ Architecture

```
+----------------------------------------------------------------------------------------+
|                                    CLIENT APPLICATION                                  |
+----------------------------------------------------------------------------------------+
                                           |
                                           v
+----------------------------------------------------------------------------------------+
|                          FastAPI Application (app.main:app)                            |
|                                                                                        |
|  [ ASGI Monitoring Middleware ]                                                        |
|     |---> Latency Tracking, Status Code Recording, IP & User-Agent Logging             |
|     |---> Automated Alert Threshold Evaluator                                          |
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
|  (WAL Mode Active)    |          | Exporter          |       | - Slack Webhook    |
|  - request_logs       |          | (Prometheus Scrape|       | - Email (SMTP)     |
|  - alerts             |          |  Format)          |       | - Twilio / SMS     |
|  - simulation_runs    |          |                   |       +--------------------+
+-----------------------+          +-------------------+
```

---

## ⚡ Quick Start

### 1. Installation
```bash
git clone https://github.com/example/fast-api-monitoring_board.git
cd fast-api-monitoring_board
pip install -r requirements.txt
```

### 2. Launch
```bash
python run.py
```
Or with Uvicorn:
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Open in Browser
- **Dashboard UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Prometheus Metrics:** [http://127.0.0.1:8000/metrics](http://127.0.0.1:8000/metrics)
- **API Health Check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🧪 Failure Simulation Matrix

| Scenario | Trigger | Expected Detection | Expected Alert | Root Cause Analysis Output |
|---|---|---|---|---|
| **1. Auth Failure** | `/api/auth/test` | 401 Unauthorized | Auth error alert | "Authentication token missing or invalid: The request lacked required 'Authorization: Bearer <token>' header or token has expired. Verify API gateway credentials." |
| **2. API Timeout** | `/simulate-timeout` | Slow response &gt;3s | Timeout alert | "Upstream dependency delayed response: Upstream database / microservice spent 3,250ms processing query before returning. Breached 3000ms SLA threshold." |
| **3. Server Error** | `/simulate-error` | HTTP 500 | Server error alert | "Internal server error — check application logs: Database transaction deadlocked while executing batch write lock in worker thread." |
| **4. Rate Limit** | `/simulate-rate-limit` | HTTP 429 | Rate limit alert | "Client exceeded allowed requests per minute: Token bucket algorithm depleted (limit: 60 req/min, burst: 10)." |

---

## 📊 Endpoints Catalog

### Core REST Service
- `GET /health`: Health status (`Healthy`, `Degraded`, `Down`), CPU, memory, active alerts.
- `GET /users`: Sample user directory.
- `GET /products`: Sample cloud products catalog.
- `GET /simulate-error`: Simulates HTTP 500 error.
- `GET /simulate-timeout`: Simulates slow latency response (>3.0s).
- `GET /simulate-rate-limit`: Simulates HTTP 429 rate limit exceeded.
- `GET /api/auth/test`: Simulates 401 Unauthorized authentication check.

### Observability & Management
- `GET /metrics`: Prometheus text exposition format.
- `GET /api/metrics/summary`: Executive dashboard metrics summary.
- `GET /api/metrics/timeseries`: Historical time-series data buckets for charts.
- `GET /api/logs`: Recent raw request logs stream.
- `GET /api/alerts`: Active and historical incident alerts.
- `POST /api/alerts/{id}/ack`: Acknowledge incident alert.
- `POST /api/alerts/clear`: Clear all alerts.
- `POST /api/simulations/run`: Execute failure simulation scenario.
- `GET /api/ai/recommendations`: AI-generated recommendations.
- `POST /api/ai/ask`: Free-form conversational SRE Q&A.
- `POST /api/notifications/test`: Test Slack, Email, and Twilio notification delivery.

---

## 🎨 Visual & Interactive Requirements Implementation

- **A. HD Animated Graphics**: Interactive 2D/3D Particle Mesh background on `<canvas id="bg-canvas">`, pulsing status beacon indicators, animated SVG ECG heartbeat line, rotating orbital scanners, and floating satellite empty states.
- **B. Background Throughout Application**: Continuous particle mesh with adaptive node styling for dark and light palettes, and frosted glass cards (`backdrop-filter: blur(16px)`).
- **C. Pop-Up / Toast Stack**: Auto-dismissing stacked notifications (4.5s countdown bar), manual dismiss button, and destructive action confirmation modals.
- **D. Web Audio API Synthesizer**: Clean synthesized frequencies for clicks, navigation, success chimes, warning thuds, error buzzes, and simulation chirps with global mute toggle.
- **E. AI Recommendations & Free-form Q&A**: Gemini 1.5 Flash integration with fallback SRE heuristics engine, interactive "Accept" and "Dismiss" buttons, and conversational chat.
- **F. Dark / Light Mode**: Seamless theme switcher in header, persisted in `localStorage`.

---

## 🧪 Testing

Run all 13 automated unit tests:
```bash
python -m pytest tests/test_api.py -v
```

Run end-to-end integration verification:
```bash
python tests/verify_all.py
```

---

## 📂 Project Structure

```
fast-api-monitoring_board/
├── app/
│   ├── main.py              # FastAPI app, routes, static mount
│   ├── config.py            # Environment & alert threshold settings
│   ├── database.py          # SQLite schema, queries, request logging
│   ├── monitoring.py        # Metrics calculator & Prometheus exporter
│   ├── alerts.py            # Alert rules evaluator & notification dispatchers
│   ├── simulation.py        # 4 Failure scenarios & Root Cause Analysis
│   ├── ai_advisor.py        # Gemini AI & SRE heuristics engine
│   └── models.py            # Pydantic schemas
├── static/
│   ├── index.html           # Production-ready dashboard UI
│   ├── app.js               # Reactive frontend logic, Web Audio, Canvas, Charts
│   ├── styles.css           # Glassmorphism, animations, dark/light theme
│   └── favicon.svg          # Glowing vector branding
├── frontend/                # Standalone React + TypeScript + Vite project
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       └── utils/audio.ts
├── tests/
│   ├── test_api.py          # Pytest suite (13 passing tests)
│   └── verify_all.py        # End-to-end verification script
├── docs/
│   ├── ARCHITECTURE.md      # Architecture diagram & data flow
│   ├── SETUP.md             # Installation, setup, and configuration
│   ├── ALERT_RULES.md       # Thresholds and notification channels
│   ├── SIMULATION_GUIDE.md  # How to run and verify failure scenarios
│   └── TROUBLESHOOTING.md   # Troubleshooting & maintenance runbook
├── requirements.txt         # Python dependencies
├── run.py                   # Single-command launcher
└── README.md                # Master documentation
```

---

## 🚀 Deploying to Vercel

NovaPulse AI is pre-configured for zero-friction Vercel deployment via `vercel.json` and `api/index.py`:

### Option A: Deploy via Vercel CLI
```bash
npm install -g vercel
vercel
```

### Option B: Deploy via GitHub / GitLab
1. Push this repository to GitHub or GitLab.
2. Visit [vercel.com/new](https://vercel.com/new) and import your repo.
3. Vercel automatically detects the Python runtime from `vercel.json` and `api/index.py`.
4. Click **Deploy**!
- On Vercel serverless functions, SQLite auto-adapts to `/tmp/monitoring.db` with non-blocking write locks.

---

## ✅ Definition of Done Checklist

- [x] FastAPI sample API created and running with all required endpoints (`/health`, `/users`, `/products`, `/simulate-error`, `/simulate-timeout`, `/simulate-rate-limit`, `/api/auth/test`)
- [x] API monitoring configured, collecting metrics, response times, and status codes in SQLite
- [x] Dashboard displays API uptime, latency, total requests, failed requests, and current status
- [x] Alerts configured (Downtime, >3s latency, HTTP 500, >5% failure rate, rate limits) with multi-channel proofs (Slack, Email, SMS)
- [x] All four failure scenarios detected with automated Root Cause Analysis (RCA) output
- [x] HD animated graphics, background particle mesh, pop-up toasts, button click sounds, AI recommendations, and dark/light mode toggle implemented
- [x] Comprehensive documentation and automated test suite completed with 100% pass rate

