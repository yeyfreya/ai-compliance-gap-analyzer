"""
Supabase tracking for user behavior and report persistence.
AI agent observability (steps, thinking, tokens) is handled by Langfuse.

All functions are fail-safe: Supabase errors are logged but never crash the app.
If SUPABASE_URL / SUPABASE_KEY are missing, tracking is silently disabled.
"""

import os
import json
from datetime import datetime, timezone
from functools import wraps

_supabase_client = None
_tracking_enabled = False


def _init_supabase():
    """Lazy-init the Supabase client on first use."""
    global _supabase_client, _tracking_enabled

    if _supabase_client is not None:
        return

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        print("ℹ️  Supabase tracking disabled (SUPABASE_URL / SUPABASE_KEY not set)")
        _tracking_enabled = False
        return

    try:
        from postgrest import SyncPostgrestClient
        _supabase_client = SyncPostgrestClient(
            f"{url}/rest/v1",
            headers={"apikey": key, "Authorization": f"Bearer {key}"},
        )
        _tracking_enabled = True
        print("✅ Supabase tracking enabled")
    except Exception as e:
        print(f"⚠️ Supabase init failed: {e}")
        _tracking_enabled = False


def _safe(fn):
    """Decorator: catch and log any Supabase error so the app never crashes."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        _init_supabase()
        if not _tracking_enabled:
            return None
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"⚠️ Supabase tracking error in {fn.__name__}: {e}")
            return None
    return wrapper


# ── Session tracking ──────────────────────────────────────────────────────────

@_safe
def init_session(streamlit_session_id: str, app_version: str) -> str | None:
    """Create a session row. Returns the session UUID."""
    result = _supabase_client.from_("sessions").insert({
        "streamlit_session_id": streamlit_session_id,
        "app_version": app_version,
    }).execute()
    return result.data[0]["id"]


# ── Analysis run tracking ─────────────────────────────────────────────────────

@_safe
def start_run(
    session_id: str | None,
    use_case: str,
    technology: str,
    industry: str,
    scenario_source: str,
    app_version: str,
) -> str | None:
    """Create an analysis_runs row with status='running'. Returns the run UUID."""
    row = {
        "use_case": use_case,
        "technology": technology,
        "industry": industry,
        "scenario_source": scenario_source,
        "app_version": app_version,
        "status": "running",
    }
    if session_id:
        row["session_id"] = session_id

    result = _supabase_client.from_("analysis_runs").insert(row).execute()
    return result.data[0]["id"]


@_safe
def complete_run(
    run_id: str,
    timing: dict,
    status: str = "completed",
    error_message: str | None = None,
) -> None:
    """Update an analysis run with final timing and status."""
    update = {
        "status": status,
        "planning_sec": timing.get("planning_sec"),
        "research_sec": timing.get("research_sec"),
        "analysis_sec": timing.get("analysis_sec"),
        "total_sec": timing.get("total_sec"),
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    if error_message:
        update["error_message"] = error_message

    _supabase_client.from_("analysis_runs").update(update).eq("id", run_id).execute()


# ── User event tracking ──────────────────────────────────────────────────────

@_safe
def log_user_event(
    session_id: str,
    event_type: str,
    run_id: str | None = None,
    event_data: dict | None = None,
) -> None:
    """Log a user interaction event."""
    row = {
        "session_id": session_id,
        "event_type": event_type,
    }
    if run_id:
        row["run_id"] = run_id
    if event_data:
        row["event_data"] = event_data

    _supabase_client.from_("user_events").insert(row).execute()


# ── Report persistence ────────────────────────────────────────────────────────

@_safe
def save_report_to_db(
    run_id: str,
    report_markdown: str,
    search_queries: list,
    report_filename: str,
) -> None:
    """Store the full report content in Supabase."""
    _supabase_client.from_("reports").insert({
        "run_id": run_id,
        "report_markdown": report_markdown,
        "search_queries": json.dumps(search_queries),
        "report_filename": report_filename,
    }).execute()
