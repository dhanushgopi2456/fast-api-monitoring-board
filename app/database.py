import sqlite3
import datetime
import os
import random
from typing import List, Dict, Any, Optional
from app.config import settings

def get_db_connection() -> sqlite3.Connection:
    db_path = settings.DATABASE_PATH
    dirname = os.path.dirname(db_path)
    if dirname and not os.path.exists(dirname):
        try:
            os.makedirs(dirname, exist_ok=True)
        except Exception:
            pass
    conn = sqlite3.connect(db_path, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Request Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS request_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        method TEXT NOT NULL,
        path TEXT NOT NULL,
        status_code INTEGER NOT NULL,
        response_time_ms REAL NOT NULL,
        client_ip TEXT,
        user_agent TEXT,
        error_message TEXT
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON request_logs(timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_status ON request_logs(status_code);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_path ON request_logs(path);")

    # 2. Alerts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        rule_name TEXT NOT NULL,
        severity TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        message TEXT NOT NULL,
        root_cause TEXT,
        remediation TEXT,
        status TEXT DEFAULT 'active',
        acknowledged_at DATETIME
    );
    """)

    # 3. Simulation Runs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulation_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        scenario_id TEXT NOT NULL,
        scenario_name TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        status_code INTEGER NOT NULL,
        duration_ms REAL NOT NULL,
        result TEXT NOT NULL,
        root_cause TEXT NOT NULL
    );
    """)

    # 4. System Metrics Snapshots
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        cpu_percent REAL,
        memory_percent REAL,
        active_connections INTEGER,
        uptime_seconds REAL
    );
    """)

    conn.commit()
    conn.close()

def log_request(method: str, path: str, status_code: int, response_time_ms: float, 
                client_ip: str = "127.0.0.1", user_agent: str = "unknown", error_message: str = None) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO request_logs (timestamp, method, path, status_code, response_time_ms, client_ip, user_agent, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (now_iso, method, path, status_code, response_time_ms, client_ip, user_agent, error_message))
    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return inserted_id

def create_alert(rule_name: str, severity: str, endpoint: str, message: str, 
                 root_cause: str = "", remediation: str = "") -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO alerts (timestamp, rule_name, severity, endpoint, message, root_cause, remediation, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
    """, (now_iso, rule_name, severity, endpoint, message, root_cause, remediation))
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return alert_id

def log_simulation(scenario_id: str, scenario_name: str, endpoint: str, 
                   status_code: int, duration_ms: float, result: str, root_cause: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO simulation_runs (timestamp, scenario_id, scenario_name, endpoint, status_code, duration_ms, result, root_cause)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (now_iso, scenario_id, scenario_name, endpoint, status_code, duration_ms, result, root_cause))
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id

def seed_sample_history(force: bool = False):
    """Seed sample historical metrics so the dashboard demonstrates trend visualizations immediately."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM request_logs")
    count = cursor.fetchone()["count"]
    
    if count > 30 and not force:
        conn.close()
        return

    now = datetime.datetime.now(datetime.timezone.utc)
    sample_endpoints = [
        ("GET", "/health", 200, (8, 25)),
        ("GET", "/users", 200, (20, 85)),
        ("GET", "/products", 200, (35, 120)),
        ("GET", "/users", 200, (18, 65)),
        ("GET", "/health", 200, (5, 15)),
        ("GET", "/products", 200, (40, 110)),
        ("GET", "/api/auth/test", 401, (12, 35)),
        ("GET", "/simulate-error", 500, (55, 180)),
        ("GET", "/simulate-rate-limit", 429, (10, 28)),
    ]

    logs_batch = []
    # Seed 120 requests over the past 2 hours
    for i in range(120, 0, -1):
        dt = now - datetime.timedelta(minutes=i)
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # 94% normal traffic, 6% anomalies
        roll = random.random()
        if roll < 0.88:
            choice = random.choice([0, 1, 2, 3, 4, 5])
            method, path, status, (l_min, l_max) = sample_endpoints[choice]
            lat = round(random.uniform(l_min, l_max), 2)
            err = None
        elif roll < 0.94:
            # 401 or 429
            choice = random.choice([6, 8])
            method, path, status, (l_min, l_max) = sample_endpoints[choice]
            lat = round(random.uniform(l_min, l_max), 2)
            err = "Unauthorized" if status == 401 else "Rate limit reached"
        elif roll < 0.98:
            # 500 error
            method, path, status, (l_min, l_max) = sample_endpoints[7]
            lat = round(random.uniform(l_min, l_max), 2)
            err = "Internal server error"
        else:
            # High latency spike
            method, path, status = "GET", "/simulate-timeout", 200
            lat = round(random.uniform(3100, 3600), 2)
            err = "Latency threshold exceeded"

        logs_batch.append((dt_str, method, path, status, lat, "127.0.0.1", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", err))

    cursor.executemany("""
        INSERT INTO request_logs (timestamp, method, path, status_code, response_time_ms, client_ip, user_agent, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, logs_batch)

    # Seed initial alerts
    cursor.execute("SELECT COUNT(*) as count FROM alerts")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("""
            INSERT INTO alerts (timestamp, rule_name, severity, endpoint, message, root_cause, remediation, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            (now - datetime.timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
            "High Response Latency",
            "WARNING",
            "/simulate-timeout",
            "Response time spiked to 3,420ms (>3000ms threshold)",
            "Simulated I/O dependency bottleneck",
            "Review database connection pooling and upstream timeouts.",
            "acknowledged"
        ))
        cursor.execute("""
            INSERT INTO alerts (timestamp, rule_name, severity, endpoint, message, root_cause, remediation, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            (now - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
            "HTTP 500 Internal Server Error",
            "CRITICAL",
            "/simulate-error",
            "HTTP 500 triggered on /simulate-error",
            "Unhandled exception simulated in worker thread",
            "Inspect stack trace and implement defensive try-except handler.",
            "active"
        ))

    conn.commit()
    conn.close()
