<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&amp;color=0:020617,35:2563EB,70:7C3AED,100:06B6D4&amp;height=240&amp;section=header&amp;text=NovaPulse%20AI&amp;fontSize=52&amp;fontColor=ffffff&amp;animation=fadeIn&amp;fontAlignY=35&amp;desc=API%20Monitoring%20%7C%20Observability%20%7C%20AI%20SRE&amp;descAlignY=56&amp;descSize=17" alt="NovaPulse AI banner" width="100%" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&amp;weight=600&amp;size=18&amp;duration=2600&amp;pause=800&amp;color=06B6D4&amp;center=true&amp;vCenter=true&amp;width=780&amp;lines=Monitor+Every+Request.;Detect+Incidents+Faster.;Simulate+Failures.+Improve+Reliability.;AI-Assisted+Site+Reliability+Engineering." alt="NovaPulse AI animated tagline" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-API%20Monitoring-009688?style=for-the-badge&amp;logo=fastapi&amp;logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Prometheus-Metrics-E6522C?style=for-the-badge&amp;logo=prometheus&amp;logoColor=white" alt="Prometheus" />
  <img src="https://img.shields.io/badge/SQLite-Storage-003B57?style=for-the-badge&amp;logo=sqlite&amp;logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Google%20Gemini-AI%20Advisor-4285F4?style=for-the-badge&amp;logo=googlegemini&amp;logoColor=white" alt="Google Gemini" />
</p>

<h1 align="center">🚀 NovaPulse AI</h1>

<p align="center">
  <strong>FastAPI API Monitoring &amp; Observability Dashboard</strong>
</p>

<p align="center">
  Monitor API health, analyze request performance, investigate incidents, and explore controlled failure scenarios through an interactive observability dashboard.
</p>

---

## 🧭 Quick Navigation

<p align="center">
  <a href="#about"><img src="https://img.shields.io/badge/About-2563EB?style=for-the-badge" alt="About" /></a>
  <a href="#features"><img src="https://img.shields.io/badge/Features-7C3AED?style=for-the-badge" alt="Features" /></a>
  <a href="#screenshots"><img src="https://img.shields.io/badge/Screenshots-DB2777?style=for-the-badge" alt="Screenshots" /></a>
  <a href="#system-architecture"><img src="https://img.shields.io/badge/System_Architecture-0891B2?style=for-the-badge" alt="System Architecture" /></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Quick_Start-16A34A?style=for-the-badge" alt="Quick Start" /></a>
  <a href="#api-endpoints"><img src="https://img.shields.io/badge/API_Endpoints-EA580C?style=for-the-badge" alt="API Endpoints" /></a>
  <a href="#testing"><img src="https://img.shields.io/badge/Testing-6366F1?style=for-the-badge" alt="Testing" /></a>
  <a href="#deployment"><img src="https://img.shields.io/badge/Deployment-0F766E?style=for-the-badge" alt="Deployment" /></a>
</p>

<p align="center">
  <a href="#system-architecture">
    <img src="https://img.shields.io/badge/🏗️_Explore_System_Architecture-7C3AED?style=for-the-badge&amp;logo=diagramsdotnet&amp;logoColor=white" alt="Explore System Architecture" />
  </a>
  <a href="#quick-start">
    <img src="https://img.shields.io/badge/▶_Run_Locally-16A34A?style=for-the-badge" alt="Run Locally" />
  </a>
</p>

---

<a id="about"></a>

## 📘 About the Project

**NovaPulse AI** is a full-stack API monitoring and observability platform for FastAPI applications.

It combines request telemetry, performance metrics, alert management, controlled failure simulations, and AI-assisted incident analysis in one dashboard.

The project includes a FastAPI backend, SQLite-based request and incident storage, interactive charts, an animated web interface, Prometheus-compatible metrics, notification integrations, and a Google Gemini-powered SRE advisor with a heuristic fallback.

### 🎯 Project Objectives

- Monitor API requests and response performance.
- Track request volume, availability, latency, and HTTP status codes.
- Detect configured error and latency thresholds.
- Simulate common API failure scenarios.
- Display incident information and root-cause analysis.
- Export metrics in Prometheus text exposition format.
- Explore AI-assisted recommendations and troubleshooting.
- Provide a responsive dashboard with dark and light themes.

---

<a id="features"></a>

## ✨ Key Features

### 📡 API Observability

- Request and response monitoring through FastAPI middleware.
- Average latency and p95 and p99 latency metrics.
- Request volume and requests-per-minute tracking.
- HTTP status-code distribution, including 2xx, 4xx, and 5xx responses.
- Availability and service-health information.
- Request logging with recorded IP and User-Agent information.

### 🚨 Incident & Alert Management

- Configurable downtime and high-latency thresholds.
- Detection of HTTP 500 errors and elevated error rates.
- Rate-limit incident simulation.
- Active and historical alert views.
- Alert acknowledgement and clearing operations.
- Notification dispatchers for Slack webhooks, SMTP email, and Twilio SMS.

### 🧪 Chaos & Failure Simulation

Explore controlled scenarios to understand how an API behaves when common failures occur:

- Authentication failure — HTTP 401.
- Slow response or timeout scenario.
- Server-side exception — HTTP 500.
- Rate-limit response — HTTP 429.

The documented simulation workflows provide diagnostic output and suggested remediation steps.

### 🤖 AI SRE Advisor

- Google Gemini 1.5 Flash integration.
- Built-in SRE heuristic fallback.
- AI-generated recommendations.
- Natural-language troubleshooting questions.
- Accept or dismiss recommendation interactions.

### 🎨 Interactive Dashboard

- Animated particle-mesh background.
- Glowing service-status indicators.
- Animated SVG heartbeat line.
- Orbital loading effects and animated empty states.
- Interactive charts with Chart.js.
- Glassmorphism cards and frosted surfaces.
- Dark and light themes with a persisted preference.
- Toast notifications and confirmation modals.
- Synthesized Web Audio API feedback with a mute control.

---

<a id="screenshots"></a>

## 📸 Screenshots

Use this section to showcase the actual interface from your running NovaPulse AI application.

<table>
  <tr>
    <td align="center" width="50%">
      <strong>📊 Monitoring Dashboard</strong><br/><br/>
      <img src="screenshots/dashboard.png" alt="NovaPulse AI monitoring dashboard" width="100%" /><br/>
      <sub>API health, requests, latency, and service metrics.</sub>
    </td>
    <td align="center" width="50%">
      <strong>📈 Metrics &amp; Analytics</strong><br/><br/>
      <img src="screenshots/metrics.png" alt="NovaPulse AI metrics and analytics" width="100%" /><br/>
      <sub>Request trends, status codes, and latency visualization.</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <strong>🚨 Incident &amp; Alerts</strong><br/><br/>
      <img src="screenshots/alerts.png" alt="NovaPulse AI incident alert center" width="100%" /><br/>
      <sub>Incident detection, alert history, and acknowledgement.</sub>
    </td>
    <td align="center" width="50%">
      <strong>🤖 AI SRE Advisor</strong><br/><br/>
      <img src="screenshots/ai-advisor.png" alt="NovaPulse AI SRE advisor" width="100%" /><br/>
      <sub>AI-assisted recommendations and troubleshooting.</sub>
    </td>
  </tr>
</table>

> **Screenshot setup:** These image paths are placeholders. Capture the real application screens, save them in the `screenshots/` directory using the filenames shown, and commit the images to your repository. Remove any entries for screens that are not present in your application.

---

<a id="system-architecture"></a>

## 🏗️ System Architecture

<p align="center">
  <a href="#system-architecture">
    <img src="https://img.shields.io/badge/🏗️_View_System_Architecture-2563EB?style=for-the-badge&amp;logo=diagramsdotnet&amp;logoColor=white" alt="View System Architecture" />
  </a>
</p>

```mermaid
flowchart TB
    USER["👤 User / Browser"] --> UI["Dashboard UI<br/>HTML · CSS · JavaScript · Chart.js"]

    UI -->|"HTTP requests"| APP["FastAPI Application"]

    subgraph CORE["Application Layer"]
        APP --> MW["Monitoring Middleware"]
        MW --> ROUTES["REST API Routes"]
        MW --> TELEMETRY["Request Telemetry"]
        ROUTES --> ALERTS["Alert Evaluator"]
        ROUTES --> SIM["Failure Simulation Engine"]
        ROUTES --> AI["AI SRE Advisor"]
    end

    TELEMETRY --> DB[("SQLite Database")]
    ALERTS --> DB

    TELEMETRY --> PROM["Prometheus Metrics Exporter"]
    PROM -->|"Scrape /metrics"| MON["Prometheus-compatible Monitoring"]

    ALERTS --> NOTIFY["Notification Dispatcher"]
    NOTIFY --> SLACK["Slack Webhook"]
    NOTIFY --> EMAIL["SMTP Email"]
    NOTIFY --> SMS["Twilio SMS"]

    AI --> GEMINI["Google Gemini"]
    AI --> FALLBACK["SRE Heuristic Fallback"]

    classDef client fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A,stroke-width:2px;
    classDef app fill:#EDE9FE,stroke:#7C3AED,color:#4C1D95,stroke-width:2px;
    classDef storage fill:#D1FAE5,stroke:#059669,color:#064E3B,stroke-width:2px;
    classDef monitoring fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
    classDef external fill:#FFEDD5,stroke:#EA580C,color:#9A3412,stroke-width:2px;

    class USER,UI client;
    class APP,MW,ROUTES,ALERTS,SIM,AI app;
    class DB storage;
    class TELEMETRY,PROM,MON monitoring;
    class NOTIFY,SLACK,EMAIL,SMS,GEMINI,FALLBACK external;
```

### 🔄 Monitoring & Incident Workflow

```mermaid
flowchart TD
    A["Incoming API Request"] --> B["Monitoring Middleware"]
    B --> C["Execute API Endpoint"]
    C --> D["Record Status and Latency"]
    D --> E["Persist Request Telemetry"]
    E --> F["Evaluate Alert Thresholds"]
    F --> G{"Threshold Breached?"}
    G -->|No| H["Update Dashboard Metrics"]
    G -->|Yes| I["Create or Update Alert"]
    I --> J["Dispatch Configured Notifications"]
    I --> K["Provide Diagnostic Context"]
    K --> L["AI Advisor or Heuristic Guidance"]
    L --> H

    classDef request fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A,stroke-width:2px;
    classDef processing fill:#EDE9FE,stroke:#7C3AED,color:#4C1D95,stroke-width:2px;
    classDef alert fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
    classDef result fill:#D1FAE5,stroke:#059669,color:#064E3B,stroke-width:2px;

    class A,B,C request;
    class D,E,F,G processing;
    class I,J,K alert;
    class H,L result;
```

> The diagrams represent the documented application design. Actual deployment topology and middleware execution order should be confirmed against the implementation.

---

<a id="tech-stack"></a>

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| Uvicorn | ASGI development server |
| SQLite | Local telemetry, alert, and simulation storage |
| Prometheus exposition | Metrics export |
| HTML5, CSS, JavaScript | Dashboard interface |
| Tailwind CSS | Utility-based styling |
| Chart.js | Interactive metrics charts |
| Web Audio API | Synthesized sound feedback |
| Google Gemini 1.5 Flash | AI-assisted SRE recommendations and Q&A |
| Pytest | Automated API tests |
| Vercel | Documented deployment target |

---

<a id="quick-start"></a>

## ⚡ Quick Start — Run Locally

### Prerequisites

Install the following tools before starting:

- Python 3.10 or a compatible version supported by your dependencies.
- Git.
- pip, included with standard Python installations.

### 1. Clone the Repository

Use your actual GitHub repository URL if it differs from the one below.

```bash
git clone https://github.com/dhanushgopi2456/fast-api-monitoring-board.git
cd fast-api-monitoring_board
```

> If the repository URL or folder name differs in your GitHub account, update these commands to match the actual repository.

### 2. Install Dependencies

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the Application

Run the project launcher:

```bash
python run.py
```

Alternatively, start FastAPI with Uvicorn:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Open the Dashboard

| Resource | Local URL |
|---|---|
| Dashboard | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Swagger API Documentation | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| Prometheus Metrics | [http://127.0.0.1:8000/metrics](http://127.0.0.1:8000/metrics) |
| API Health Check | [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) |

---

<a id="failure-simulations"></a>

## 🧪 Failure Simulation Matrix

NovaPulse AI documents four scenarios for exploring API error detection and diagnostic guidance.

| Scenario | Trigger | Expected Behavior | Diagnostic Focus |
|---|---|---|---|
| Authentication Failure | `/api/auth/test` | HTTP 401 | Missing or invalid authentication |
| Slow Response | `/simulate-timeout` | Response delay exceeding 3 seconds | Latency threshold breach |
| Server Error | `/simulate-error` | HTTP 500 | Server-side failure investigation |
| Rate Limit | `/simulate-rate-limit` | HTTP 429 | Request quota or rate-limit behavior |

### Example Root-Cause Analysis Areas

- **HTTP 401:** Inspect the Authorization header and authentication configuration.
- **Slow response:** Investigate dependency latency and slow database or service operations.
- **HTTP 500:** Review application logs and exception details.
- **HTTP 429:** Inspect request frequency, configured quotas, and client retry behavior.

The exact incident text and root-cause messages depend on the application's configured simulations.

> **Safety:** Run failure simulations against your local or authorized test environment. These endpoints deliberately generate error responses and should not be exposed without suitable safeguards on production systems.

---

<a id="api-endpoints"></a>

## 📋 API Endpoints Catalog

### Core REST Service

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health status and system metrics |
| `GET` | `/users` | Sample user directory |
| `GET` | `/products` | Sample product catalog |
| `GET` | `/simulate-error` | Simulate an HTTP 500 response |
| `GET` | `/simulate-timeout` | Simulate a slow response |
| `GET` | `/simulate-rate-limit` | Simulate HTTP 429 |
| `GET` | `/api/auth/test` | Simulate an HTTP 401 authentication check |

### Observability & Incident Management

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/metrics` | Prometheus text exposition metrics |
| `GET` | `/api/metrics/summary` | Dashboard summary metrics |
| `GET` | `/api/metrics/timeseries` | Historical time-series buckets |
| `GET` | `/api/logs` | Recent request logs |
| `GET` | `/api/alerts` | Active and historical alerts |
| `POST` | `/api/alerts/{id}/ack` | Acknowledge an alert |
| `POST` | `/api/alerts/clear` | Clear alerts |
| `POST` | `/api/simulations/run` | Run a failure simulation |
| `GET` | `/api/ai/recommendations` | Retrieve AI recommendations |
| `POST` | `/api/ai/ask` | Submit a natural-language SRE question |
| `POST` | `/api/notifications/test` | Test configured notification channels |

### Explore the API Interactively

Open the Swagger UI after starting the application:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Use it to inspect the registered endpoints, review request formats, and send test requests.

---

<a id="alerting"></a>

## 🚨 Alerting & Notifications

The project documents alert evaluation for the following conditions:

| Condition | Documented Threshold |
|---|---|
| Slow response | More than 3 seconds |
| Server error | HTTP 500 |
| Error-rate increase | More than 5% |
| Service downtime | Detected downtime |
| Rate limiting | HTTP 429 or rate-limit scenario |

### Supported Notification Integrations

- **Slack:** Webhook-based notifications.
- **Email:** SMTP-based delivery.
- **SMS:** Twilio integration.

Configuration, credentials, and delivery behavior depend on the implementation and environment settings. Keep webhook URLs, SMTP passwords, and Twilio credentials out of source control.

---

<a id="ai-advisor"></a>

## 🤖 AI SRE Advisor

The AI advisor combines telemetry context with diagnostic assistance.

Documented capabilities include:

- Generating troubleshooting recommendations.
- Answering free-form SRE questions.
- Suggesting diagnostic next steps.
- Falling back to built-in heuristic guidance when the AI integration is unavailable.
- Allowing users to accept or dismiss recommendations in the dashboard.

### AI Configuration

The documented integration uses Google Gemini 1.5 Flash. If API-key configuration is required by your local setup, configure it using the environment-variable names expected by your actual code.

For production usage, validate AI-generated suggestions before applying them. Treat outputs as assistance rather than a substitute for reviewing logs, metrics, and application behavior.

---

<a id="visual-implementation"></a>

## 🎨 Visual & Interactive Experience

The README documents these interface features:

- **Animated canvas:** Particle mesh background.
- **Status beacons:** Pulsing service-status indicators.
- **Heartbeat animation:** SVG ECG-style vital line.
- **Loading states:** Orbital scanners and animated indicators.
- **Notifications:** Stacked toast messages with countdown bars.
- **Confirmation dialogs:** Confirmation for destructive actions.
- **Audio feedback:** Synthesized click, navigation, success, warning, and error sounds.
- **Theme switching:** Dark and light palettes with a persisted preference.
- **Glassmorphism:** Frosted surfaces and blurred backgrounds.
- **Interactive analytics:** Chart.js charts and visual telemetry summaries.

These features aim to make operational information easier to explore while preserving the utility of the underlying API.

---

<a id="testing"></a>

## 🧪 Testing

### Run the Pytest Suite

The original project README documents 13 API tests.

```bash
python -m pytest tests/test_api.py -v
```

### Run End-to-End Verification

```bash
python tests/verify_all.py
```

### Testing Areas

The project documentation describes testing and verification of:

- API health and core routes.
- Monitoring and metrics endpoints.
- Alert behavior.
- Failure simulation scenarios.
- Dashboard-related API workflows.

Run the tests in your current environment to confirm the actual results. A previously documented pass rate should not be treated as a fresh test result.

---

<a id="project-structure"></a>

## 📂 Project Structure

```text
fast-api-monitoring_board/
├── app/
│   ├── main.py              # FastAPI application, routes, static mounts
│   ├── config.py            # Configuration and alert thresholds
│   ├── database.py          # SQLite schema, queries, request logging
│   ├── monitoring.py        # Metrics calculation and exporter
│   ├── alerts.py             # Alert evaluation and notifications
│   ├── simulation.py         # Failure scenarios and RCA
│   ├── ai_advisor.py         # Gemini integration and heuristic fallback
│   └── models.py             # Pydantic schemas
├── static/
│   ├── index.html            # Dashboard UI
│   ├── app.js                # Frontend behavior, audio, canvas, charts
│   ├── styles.css            # Styling, animation, themes
│   └── favicon.svg           # Vector branding
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       └── utils/audio.ts
├── tests/
│   ├── test_api.py            # API test suite
│   └── verify_all.py          # End-to-end verification
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   ├── ALERT_RULES.md
│   ├── SIMULATION_GUIDE.md
│   └── TROUBLESHOOTING.md
├── requirements.txt
├── run.py
└── README.md
```

This structure follows the organization documented for the project. If the current repository differs, update the tree to match its actual files.

---

<a id="deployment"></a>

## ☁️ Deployment

The original project documentation describes a Vercel deployment configuration using `vercel.json` and `api/index.py`.

### Option A — Deploy with Vercel CLI

Install the Vercel CLI:

```bash
npm install -g vercel
```

From the project root, run:

```bash
vercel
```

Follow the CLI prompts to configure the project.

### Option B — Deploy Through the Vercel Dashboard

1. Push your project to GitHub.
2. Visit [Vercel New Project](https://vercel.com/new).
3. Import the repository.
4. Review the Python runtime configuration and entry point.
5. Configure required environment variables.
6. Deploy and inspect the build logs.

### Deployment Considerations

- SQLite data may be ephemeral in serverless environments.
- The documented configuration uses `/tmp/monitoring.db` for SQLite on Vercel.
- `/tmp` storage should not be treated as durable long-term storage.
- External API credentials must be configured securely.
- Validate that metrics, alerts, notification integrations, and AI requests work in the deployed environment.
- Ensure that failure simulation endpoints cannot be abused by unauthorized users.

Deployment success depends on the current repository configuration, runtime compatibility, and hosting platform support.

---

<a id="security"></a>

## 🔐 Security & Operational Considerations

Before exposing the dashboard to external users:

- Protect diagnostic and management endpoints with suitable access controls.
- Avoid returning sensitive request headers, IP data, or internal exception details to unauthorized users.
- Store integration credentials in environment variables or a secrets manager.
- Apply rate limits to endpoints that trigger expensive operations or notifications.
- Restrict failure simulations to authorized environments.
- Validate and sanitize incoming request data.
- Review log retention and personally identifiable information handling.
- Treat AI-generated diagnostics as untrusted suggestions that require verification.

These are recommended operational checks; they do not imply that every item is already implemented.

---

<a id="definition-of-done"></a>

## ✅ Project Checklist

The original README documents the following completion checklist:

- [x] FastAPI sample API and documented core endpoints.
- [x] Request metrics and response-time collection.
- [x] SQLite-based telemetry storage.
- [x] Dashboard metrics and service-status display.
- [x] Alert rules and notification integrations.
- [x] Four documented failure simulation scenarios.
- [x] Root-cause analysis output.
- [x] Animated graphics, notification toasts, and audio feedback.
- [x] AI recommendations and dark/light mode.
- [x] Documentation and automated tests.

Run the application and test suite to verify the current state before describing these items as independently validated.

---

## 📚 Additional Documentation

The repository's documented `docs/` directory includes:

| Document | Purpose |
|---|---|
| `ARCHITECTURE.md` | Architecture and data flow |
| `SETUP.md` | Installation and configuration |
| `ALERT_RULES.md` | Alert thresholds and channels |
| `SIMULATION_GUIDE.md` | Failure simulation workflows |
| `TROUBLESHOOTING.md` | Troubleshooting and maintenance |

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&amp;color=0:020617,50:7C3AED,100:06B6D4&amp;height=4&amp;section=footer" alt="" width="100%" />
</p>

<p align="center">
  <strong>⚡ Observe. Diagnose. Improve. Repeat.</strong><br/>
  Turning API telemetry into actionable operational insight.
</p>

<p align="center">
  <a href="https://github.com/dhanushgopi2456">
    <img src="https://img.shields.io/badge/GitHub-Dhanush%20Gopi-181717?style=for-the-badge&amp;logo=github&amp;logoColor=white" alt="GitHub Profile" />
  </a>
  <a href="https://www.linkedin.com/in/dhanush-gopi-kavala-a460a528b/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&amp;logo=linkedin&amp;logoColor=white" alt="LinkedIn Profile" />
  </a>
</p>
