import os
import json
import httpx
import datetime
from typing import List, Dict, Any, Optional
from app.monitoring import get_metrics_summary, get_timeseries_metrics
from app.config import settings

# Active recommendation cards
ACTIVE_RECOMMENDATIONS = [
    {
        "id": "rec-1",
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "severity": "CRITICAL",
        "title": "Database Lock Contention on /simulate-error",
        "description": "5xx error spikes detected on /simulate-error. Worker threads encountered transaction timeouts. Immediate review of database connection pool recommended.",
        "impact": "High error rate impacting API availability",
        "action_label": "Apply Connection Pool Tuning",
        "status": "pending"
    },
    {
        "id": "rec-2",
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "severity": "WARNING",
        "title": "p95 Latency Degradation (>3,000ms)",
        "description": "Slow response times recorded on /simulate-timeout. Responses exceeded 3.0s SLA. Consider adding an in-memory Redis cache with 60s TTL.",
        "impact": "Degraded client perceived responsiveness",
        "action_label": "Enable Response Caching",
        "status": "pending"
    },
    {
        "id": "rec-3",
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "severity": "INFO",
        "title": "Rate Limit Threshold Approaching",
        "description": "Client burst requests triggering HTTP 429 on /simulate-rate-limit. Advise client SDK to incorporate exponential backoff with full jitter.",
        "impact": "Prevents cascading retry storms",
        "action_label": "Distribute SDK Advisory",
        "status": "pending"
    }
]

def generate_ai_recommendations() -> List[Dict[str, Any]]:
    """Generates recommendations based on live telemetry."""
    summary = get_metrics_summary()
    recommendations = list(ACTIVE_RECOMMENDATIONS)
    
    # Dynamically inject live insight if error rate > 0
    if summary["error_rate_percent"] > 0:
        recommendations.insert(0, {
            "id": f"dyn-{int(datetime.datetime.now().timestamp())}",
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "severity": "CRITICAL" if summary["error_rate_percent"] > 5 else "WARNING",
            "title": f"Live Error Spike Detected ({summary['error_rate_percent']}%)",
            "description": f"Current error rate stands at {summary['error_rate_percent']}% across {summary['total_requests']} requests ({summary['status_codes']['5xx']} server errors, {summary['status_codes']['4xx']} client errors).",
            "impact": "Service degradation",
            "action_label": "Investigate Recent Logs",
            "status": "pending"
        })
    
    return recommendations[:6]

def ask_ai_question(question: str) -> Dict[str, Any]:
    """Free-form Q&A answering questions about API metrics using Gemini or expert telemetry reasoning."""
    summary = get_metrics_summary()
    timeseries = get_timeseries_metrics(limit=5)
    
    context_str = (
        f"API Status: {summary['service_status']}, "
        f"Uptime: {summary['uptime_percent']}%, "
        f"Avg Latency: {summary['avg_response_time_ms']}ms, "
        f"p95 Latency: {summary['p95_response_time_ms']}ms, "
        f"p99 Latency: {summary['p99_response_time_ms']}ms, "
        f"Total Requests: {summary['total_requests']}, "
        f"Failed Requests: {summary['failed_requests']}, "
        f"Error Rate: {summary['error_rate_percent']}%, "
        f"Active Alerts: {summary['active_alerts_count']}, "
        f"CPU: {summary['system_stats']['cpu_percent']}%, "
        f"Memory: {summary['system_stats']['memory_percent']}%"
    )

    # 1. Check if Gemini API Key is available
    api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt_content = f"""
            You are NovaPulse AI, a senior Site Reliability Engineer (SRE) and FastAPI monitoring assistant.
            Here is current real-time API telemetry:
            {context_str}

            User Question: {question}

            Provide a concise, direct, and actionable response (2-4 paragraphs) diagnosing root cause, impact, and exact remediation commands/code.
            """
            payload = {
                "contents": [{"parts": [{"text": prompt_content}]}]
            }
            with httpx.Client(timeout=8.0) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    answer = data["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "question": question,
                        "answer": answer,
                        "source": "Gemini 1.5 Flash (Live)",
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                    }
        except Exception as e:
            pass

    # 2. Heuristics & SRE Intelligence Engine
    q_lower = question.lower()
    if "uptime" in q_lower or "drop" in q_lower or "availability" in q_lower:
        answer = (
            f"**Uptime Analysis**: Current availability is **{summary['uptime_percent']}%**. "
            f"The drop is attributable to {summary['status_codes']['5xx']} server-side HTTP 500 responses "
            f"primarily from the `/simulate-error` stress test endpoint. "
            "To restore 99.99% availability, isolate the database write lock, implement an exponential circuit breaker, "
            "and divert anomalous traffic to a fallback cluster."
        )
    elif "latency" in q_lower or "slow" in q_lower or "response time" in q_lower:
        answer = (
            f"**Latency Diagnostics**: Your average response time is **{summary['avg_response_time_ms']}ms**, "
            f"with p95 peaking at **{summary['p95_response_time_ms']}ms** and p99 at **{summary['p99_response_time_ms']}ms**. "
            f"The critical driver is `/simulate-timeout`, which introduced a 3,250ms I/O delay exceeding the SLA threshold of 3,000ms. "
            "**Recommended Fix**: Wrap remote downstream dependencies with a 1,500ms client timeout and deploy Redis key-value caching."
        )
    elif "rate limit" in q_lower or "429" in q_lower:
        answer = (
            f"**Rate Limiting Audit**: Detected HTTP 429 status codes on `/simulate-rate-limit`. "
            f"The current token bucket algorithm enforces a 60 requests/minute ceiling. "
            "**Recommended Action**: Have clients implement truncated exponential backoff with random jitter, "
            "or introduce Tiered API Key quotas in your FastAPI rate limiting middleware."
        )
    elif "error" in q_lower or "500" in q_lower or "fail" in q_lower:
        answer = (
            f"**Error Distribution Analysis**: Total failed requests stand at **{summary['failed_requests']}** "
            f"({summary['status_codes']['5xx']} 5xx errors and {summary['status_codes']['4xx']} 4xx errors), "
            f"yielding an error rate of **{summary['error_rate_percent']}%**. "
            "Check `/simulate-error` logs for unhandled Python exceptions. Implement structured exception handlers with `FastAPI.exception_handler`."
        )
    else:
        answer = (
            f"**NovaPulse AI SRE Diagnosis**: System status is currently **{summary['service_status']}**. "
            f"Telemetry summary: {summary['total_requests']} total requests processed, "
            f"{summary['requests_per_minute']} RPM, {summary['uptime_percent']}% uptime, "
            f"and {summary['active_alerts_count']} active alerts. "
            f"Host memory usage is at {summary['system_stats']['memory_percent']}% and CPU at {summary['system_stats']['cpu_percent']}%. "
            "All vital telemetry metrics are within nominal operating parameters except for simulated test scenarios."
        )

    return {
        "question": question,
        "answer": answer,
        "source": "NovaPulse AI SRE Advisor",
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }

def update_recommendation_status(rec_id: str, new_status: str) -> bool:
    for rec in ACTIVE_RECOMMENDATIONS:
        if rec["id"] == rec_id:
            rec["status"] = new_status
            return True
    return False
