"""
FastAPI API Monitoring Board - Application Launcher
Runs Uvicorn server on http://127.0.0.1:8000
"""

import sys
import os
import uvicorn
from app.database import init_db, seed_sample_history

def main():
    port = int(os.getenv("PORT", "8000"))
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    print("=" * 70)
    print("  NOVAPULSE AI - FASTAPI API MONITORING BOARD")
    print("=" * 70)
    
    # 1. Initialize SQLite schema & seed baseline traffic
    print(">>> Initializing SQLite database (monitoring.db)...")
    init_db()
    seed_sample_history()
    print(">>> Database ready.")

    print("\nAvailable Services:")
    print(f"  * Web Dashboard:       http://127.0.0.1:{port}/")
    print(f"  * Interactive Docs:    http://127.0.0.1:{port}/docs")
    print(f"  * Prometheus Metrics:  http://127.0.0.1:{port}/metrics")
    print(f"  * API Health Check:    http://127.0.0.1:{port}/health")
    print("\nStarting Uvicorn ASGI server...")
    print("=" * 70)

    # 2. Run Uvicorn server
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()

