"""
Test script for v0.4 observability — verifies:
1. Supabase connection (sessions, runs, events, reports)
2. Langfuse connection (basic trace)
3. Parent trace architecture (run_id correlation across Streamlit → Supabase → Langfuse → local)

Run: python test_tracking.py
"""

import os
import json
import csv
from dotenv import load_dotenv
load_dotenv()


def test_supabase():
    """Test basic Supabase CRUD operations."""
    print("\n--- Test 1: Supabase Connection ---")
    import tracking
    tracking._init_supabase()

    if not tracking._tracking_enabled:
        print("[FAIL] Supabase not enabled -- check SUPABASE_URL and SUPABASE_KEY in .env")
        return False, None, None

    from tracking import init_session, start_run, complete_run, log_user_event, save_report_to_db

    session_id = init_session("test-session-correlation", "v0.4")
    if not session_id:
        print("[FAIL] Session insert failed")
        return False, None, None
    print(f"[PASS] Session created: {session_id}")

    run_id = start_run(session_id, "correlation test", "test tech", "test industry", "test", "v0.4")
    if not run_id:
        print("[FAIL] Analysis run insert failed")
        return False, session_id, None
    print(f"[PASS] Analysis run created: {run_id}")

    timing = {"planning_sec": 1.0, "research_sec": 2.0, "analysis_sec": 3.0, "total_sec": 6.0}
    complete_run(run_id, timing)
    print("[PASS] Analysis run completed")

    log_user_event(session_id, "test_correlation", run_id=run_id,
                   event_data={"source": "test_tracking.py", "test": "parent_trace_correlation"})
    print("[PASS] User event logged with run_id")

    save_report_to_db(run_id, "# Correlation Test Report\nThis tests run_id linking.",
                      ["test query 1"], "test_correlation_report.md")
    print("[PASS] Report saved to DB with run_id")

    # Verify cross-table linkage
    run_row = tracking._supabase_client.from_("analysis_runs").select("*").eq("id", run_id).execute()
    report_row = tracking._supabase_client.from_("reports").select("*").eq("run_id", run_id).execute()
    event_rows = tracking._supabase_client.from_("user_events").select("*").eq("run_id", run_id).execute()

    if run_row.data and run_row.data[0]["session_id"] == session_id:
        print(f"[PASS] analysis_runs.session_id links to session: {session_id}")
    else:
        print("[FAIL] analysis_runs.session_id mismatch")
        return False, session_id, run_id

    if report_row.data and report_row.data[0]["run_id"] == run_id:
        print(f"[PASS] reports.run_id links to run: {run_id}")
    else:
        print("[FAIL] reports.run_id mismatch")
        return False, session_id, run_id

    if event_rows.data:
        print(f"[PASS] user_events found {len(event_rows.data)} event(s) linked to run_id")
    else:
        print("[FAIL] No user_events found for run_id")
        return False, session_id, run_id

    print("\n[PASS] All Supabase tests passed -- cross-table linkage verified")
    return True, session_id, run_id


def test_langfuse():
    """Test Langfuse client init and basic tracing."""
    print("\n--- Test 2: Langfuse Connection ---")
    from langfuse import get_client, observe
    lf = get_client()
    if not lf:
        print("[FAIL] Langfuse client failed -- check LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST in .env")
        return False

    @observe()
    def test_traced_function(x):
        return x * 2

    result = test_traced_function(21)
    print(f"[PASS] Traced function returned: {result}")

    lf.flush()
    print("[PASS] Langfuse data flushed")
    print("\n[PASS] All Langfuse tests passed")
    return True


def test_parent_trace(run_id, session_id):
    """Test parent trace architecture: @observe wraps child spans, tagged with run_id."""
    print("\n--- Test 3: Parent Trace Architecture ---")
    from langfuse import observe, get_client
    from opentelemetry import trace as otel_trace

    lf = get_client()

    @observe()
    def mock_step_a(x):
        return x + 1

    @observe()
    def mock_step_b(x):
        return x * 2

    @observe(name="test_parent_pipeline")
    def mock_pipeline(run_id, session_id):
        span = otel_trace.get_current_span()
        span.set_attribute("session.id", str(session_id or ""))
        span.set_attribute("langfuse.trace.metadata", json.dumps({
            "supabase_run_id": str(run_id or ""),
            "supabase_session_id": str(session_id or ""),
            "test": True,
        }))
        span.set_attribute("langfuse.trace.tags", json.dumps(["test", "v0.4"]))

        trace_id = lf.get_current_trace_id()

        a = mock_step_a(10)
        b = mock_step_b(a)
        return {"result": b, "langfuse_trace_id": trace_id}

    output = mock_pipeline(run_id, session_id)
    print(f"[PASS] Parent pipeline returned: {output['result']} (expected 22)")

    if output["result"] != 22:
        print(f"[FAIL] Expected 22, got {output['result']}")
        return False

    trace_id = output.get("langfuse_trace_id")
    if trace_id:
        print(f"[PASS] Langfuse trace ID captured: {trace_id}")
    else:
        print("[WARN] Langfuse trace ID is None -- trace may still be created, check dashboard")

    lf.flush()
    print("[PASS] Parent trace flushed to Langfuse")
    print("\n[PASS] Parent trace test passed")
    print("       Check Langfuse dashboard: look for 'test_parent_pipeline' trace")
    print(f"       It should have metadata: supabase_run_id={run_id}")
    print("       And two child spans: mock_step_a, mock_step_b")
    return True


def test_local_report_correlation(run_id):
    """Test that save_report and append_test_log correctly embed run_id."""
    print("\n--- Test 4: Local Report Correlation ---")
    from agent import save_report, append_test_log

    test_result = {
        "use_case": "correlation test",
        "technology": "test tech",
        "industry": "test industry",
        "search_queries": ["test query"],
        "analysis": "# Test Analysis\nCorrelation test content.",
        "timing": {"planning_sec": 1.0, "research_sec": 2.0, "analysis_sec": 3.0, "total_sec": 6.0},
    }

    report_path = save_report(test_result, version="v0.4", run_id=run_id)
    print(f"[PASS] Report saved: {os.path.basename(report_path)}")

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    if f"**Run ID:** `{run_id}`" in content:
        print(f"[PASS] run_id found in report header")
    else:
        print("[FAIL] run_id NOT found in report header")
        return False

    append_test_log(test_result, version="v0.4", report_path=report_path, run_id=run_id)
    print("[PASS] test-log.csv appended")

    log_path = os.path.join(os.path.dirname(report_path), "test-log.csv")
    with open(log_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    last_row = rows[-1]
    if "run_id" not in reader.fieldnames:
        print("[FAIL] run_id column missing from CSV header")
        return False

    if last_row.get("run_id") == run_id:
        print(f"[PASS] run_id found in test-log.csv last row")
    else:
        print(f"[FAIL] run_id mismatch in CSV: expected {run_id}, got {last_row.get('run_id')}")
        return False

    # Clean up test report
    os.remove(report_path)
    print(f"[PASS] Test report cleaned up")

    print("\n[PASS] Local report correlation test passed")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("v0.4 Observability & Correlation Test")
    print("=" * 60)

    supabase_ok, session_id, run_id = test_supabase()
    langfuse_ok = test_langfuse()

    parent_ok = False
    local_ok = False

    if supabase_ok and langfuse_ok and run_id:
        parent_ok = test_parent_trace(run_id, session_id)
        local_ok = test_local_report_correlation(run_id)
    elif not run_id:
        print("\n[SKIP] Parent trace & local tests -- Supabase run_id required")

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    tests = [
        ("Supabase connection + cross-table linkage", supabase_ok),
        ("Langfuse connection + basic trace", langfuse_ok),
        ("Parent trace architecture (nested spans + metadata)", parent_ok),
        ("Local report correlation (run_id in report + CSV)", local_ok),
    ]
    for name, passed in tests:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")

    print("=" * 60)

    if all(ok for _, ok in tests):
        print("\nAll tests passed. Verify in dashboards:")
        print("  Supabase: Dashboard > Table Editor > sessions/analysis_runs/reports")
        print("  Langfuse: https://cloud.langfuse.com > Traces > look for 'test_parent_pipeline'")
        print(f"\n  Correlation key: run_id = {run_id}")
        print(f"  This run_id should appear in: Supabase, Langfuse trace metadata, local report header, test-log.csv")
