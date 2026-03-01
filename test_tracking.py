"""
Test script for v0.4–v0.5 observability — verifies:
1. Supabase connection (sessions, runs, events, reports)
2. Langfuse connection (basic trace)
3. Parent trace architecture (run_id correlation across Streamlit → Supabase → Langfuse → local)
4. Local report correlation (run_id in report header + CSV)
5. Error logging to Supabase (error_logs table)
6. Rate limiting (per-session analysis count)

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


def test_error_logging(session_id, run_id):
    """Test v0.5 error logging to Supabase error_logs table."""
    print("\n--- Test 5: Error Logging (v0.5) ---")
    import tracking
    from tracking import log_error, mark_run_failed

    test_error = ValueError("Test error for v0.5 integration test")

    log_error(
        test_error,
        session_id=session_id,
        run_id=run_id,
        pipeline_step="test_step",
        user_inputs={"use_case": "test", "technology": "test", "industry": "test"},
        app_version="v0.5",
    )

    rows = (tracking._supabase_client
            .from_("error_logs")
            .select("*")
            .eq("run_id", run_id)
            .execute())

    if not rows.data:
        print("[FAIL] No error_logs row found for run_id")
        return False

    row = rows.data[0]
    checks = [
        ("error_type", row.get("error_type") == "ValueError"),
        ("error_message", "Test error" in row.get("error_message", "")),
        ("pipeline_step", row.get("pipeline_step") == "test_step"),
        ("session_id", row.get("session_id") == session_id),
        ("app_version", row.get("app_version") == "v0.5"),
        ("user_inputs", row.get("user_inputs") is not None),
    ]

    all_ok = True
    for field, ok in checks:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"  {status} error_logs.{field}")
        if not ok:
            all_ok = False

    # Test mark_run_failed — create a separate run so we don't pollute the main test run
    fail_run_id = tracking._supabase_client.from_("analysis_runs").insert({
        "session_id": session_id,
        "use_case": "fail test",
        "technology": "test",
        "industry": "test",
        "scenario_source": "test",
        "app_version": "v0.5",
        "status": "running",
    }).execute().data[0]["id"]

    mark_run_failed(fail_run_id, test_error)

    fail_row = (tracking._supabase_client
                .from_("analysis_runs")
                .select("status, error_message")
                .eq("id", fail_run_id)
                .execute())

    if fail_row.data and fail_row.data[0]["status"] == "error":
        print(f"  [PASS] mark_run_failed: status='error'")
    else:
        print(f"  [FAIL] mark_run_failed: status not updated")
        all_ok = False

    if fail_row.data and "Test error" in (fail_row.data[0].get("error_message") or ""):
        print(f"  [PASS] mark_run_failed: error_message contains error text")
    else:
        print(f"  [FAIL] mark_run_failed: error_message missing")
        all_ok = False

    if all_ok:
        print("\n[PASS] All error logging tests passed")
    return all_ok


def test_rate_limiting(session_id):
    """Test v0.5 rate limiting via Supabase count query."""
    print("\n--- Test 6: Rate Limiting (v0.5) ---")
    from tracking import is_rate_limited, MAX_RUNS_PER_SESSION
    import tracking

    rate = is_rate_limited(session_id)

    if rate is None:
        print("[FAIL] is_rate_limited returned None")
        return False

    print(f"  Session {session_id[:8]}… has {rate['used']} runs (limit: {rate['limit']})")
    print(f"  [PASS] is_rate_limited returned: allowed={rate['allowed']}, used={rate['used']}, limit={rate['limit']}")

    if rate["limit"] == MAX_RUNS_PER_SESSION:
        print(f"  [PASS] Limit matches MAX_RUNS_PER_SESSION ({MAX_RUNS_PER_SESSION})")
    else:
        print(f"  [FAIL] Limit mismatch: expected {MAX_RUNS_PER_SESSION}, got {rate['limit']}")
        return False

    # Test with a fresh session that has zero runs
    fresh_session_id = tracking._supabase_client.from_("sessions").insert({
        "streamlit_session_id": "test-rate-limit-fresh",
        "app_version": "v0.5",
    }).execute().data[0]["id"]

    fresh_rate = is_rate_limited(fresh_session_id)
    if fresh_rate["allowed"] and fresh_rate["used"] == 0:
        print(f"  [PASS] Fresh session: allowed=True, used=0")
    else:
        print(f"  [FAIL] Fresh session should have 0 runs and be allowed")
        return False

    print("\n[PASS] All rate limiting tests passed")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("v0.5 Observability, Error Logging & Rate Limiting Test")
    print("=" * 60)

    supabase_ok, session_id, run_id = test_supabase()
    langfuse_ok = test_langfuse()

    parent_ok = False
    local_ok = False
    error_ok = False
    rate_ok = False

    if supabase_ok and langfuse_ok and run_id:
        parent_ok = test_parent_trace(run_id, session_id)
        local_ok = test_local_report_correlation(run_id)
    elif not run_id:
        print("\n[SKIP] Parent trace & local tests -- Supabase run_id required")

    if supabase_ok and session_id and run_id:
        error_ok = test_error_logging(session_id, run_id)
        rate_ok = test_rate_limiting(session_id)
    elif not supabase_ok:
        print("\n[SKIP] Error logging & rate limiting tests -- Supabase required")

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    tests = [
        ("Supabase connection + cross-table linkage", supabase_ok),
        ("Langfuse connection + basic trace", langfuse_ok),
        ("Parent trace architecture (nested spans + metadata)", parent_ok),
        ("Local report correlation (run_id in report + CSV)", local_ok),
        ("Error logging to Supabase (error_logs + mark_run_failed)", error_ok),
        ("Rate limiting (per-session count)", rate_ok),
    ]
    for name, passed in tests:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")

    print("=" * 60)

    if all(ok for _, ok in tests):
        print("\nAll tests passed. Verify in dashboards:")
        print("  Supabase: Dashboard > Table Editor > sessions/analysis_runs/reports/error_logs")
        print("  Langfuse: https://cloud.langfuse.com > Traces > look for 'test_parent_pipeline'")
        print(f"\n  Correlation key: run_id = {run_id}")
        print(f"  This run_id should appear in: Supabase (runs, reports, error_logs), Langfuse, local report, CSV")
