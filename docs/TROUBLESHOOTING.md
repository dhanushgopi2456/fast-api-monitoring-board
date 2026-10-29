# Troubleshooting & Maintenance Runbook

## 1. Common Issues & Solutions

### A. Port 8000 Already in Use
**Symptom:** `OSError: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`  
**Solution:** Start Uvicorn on an alternative port:
```bash
python -m uvicorn app.main:app --port 8080 --reload
```

---

### B. Database Locked or Corrupted
**Symptom:** `sqlite3.OperationalError: database is locked`  
**Solution:**
1. Stop any lingering background processes:
   ```powershell
   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
   ```
2. Remove the SQLite database and allow the application to recreate a fresh copy:
   ```bash
   rm monitoring.db
   python run.py
   ```

---

### C. Web Audio API Click Sounds Not Playing
**Symptom:** No sound heard when clicking buttons.  
**Explanation:** Modern browsers (Chrome, Edge, Safari) require user interaction (first click on the page) before the browser's `AudioContext` is allowed to output audio.  
**Solution:** Click anywhere on the dashboard or click the speaker icon in the top header. Ensure the speaker icon displays active waves and is not muted.

---

### D. Enabling Live Google Gemini AI Recommendations
**Symptom:** AI recommendations say "Antigravity SRE Neural Advisor" instead of "Gemini 1.5 Flash".  
**Explanation:** The application falls back gracefully to its built-in rule-based SRE intelligence engine when no external API key is provided.  
**Solution:** Set the `GEMINI_API_KEY` environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSy..."

# Linux / macOS
export GEMINI_API_KEY="AIzaSy..."
```

---

## 2. Maintenance & Operations

### Routine SQLite Database Vacuum
To reclaim unused disk space from old request logs:
```bash
python -c "import sqlite3; conn = sqlite3.connect('monitoring.db'); conn.execute('VACUUM;'); conn.close(); print('Vacuum complete.')"
```

### Scraping Metrics with Prometheus
Add the following job to your `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'fastapi-monitoring'
    scrape_interval: 5s
    static_configs:
      - targets: ['127.0.0.1:8000']
    metrics_path: '/metrics'
```

