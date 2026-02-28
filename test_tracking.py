"""
Test script for v0.4 observability — verifies Supabase and Langfuse connections.
Run: python test_tracking.py
"""

from dotenv import load_dotenv
load_dotenv()

def test_supabase():
    print("\n--- Testing Supabase ---")
    import tracking
    tracking._init_supabase()

    if not tracking._tracking_enabled:
        print("❌ Supabase not enabled — check SUPABASE_URL and SUPABASE_KEY in .env")
        return False

    # Test insert into sessions
    from tracking import init_session
    session_id = init_session("test-session-001", "v0.4")
    if session_id:
        print(f"✅ Session created: {session_id}")
    else:
        print("❌ Session insert failed")
        return False

    # Test user event
    from tracking import log_user_event
    log_user_event(session_id, "test_event", event_data={"source": "test_tracking.py"})
    print("✅ User event logged")

    # Test analysis run
    from tracking import start_run, complete_run
    run_id = start_run(session_id, "test use case", "test tech", "test industry", "test", "v0.4")
    if run_id:
        print(f"✅ Analysis run created: {run_id}")
        complete_run(run_id, {"planning_sec": 1.0, "research_sec": 2.0, "analysis_sec": 3.0, "total_sec": 6.0})
        print("✅ Analysis run completed")
    else:
        print("❌ Analysis run insert failed")
        return False

    # Test report persistence
    from tracking import save_report_to_db
    save_report_to_db(run_id, "# Test Report\nThis is a test.", ["test query 1"], "test_report.md")
    print("✅ Report saved to DB")

    # Verify data is readable
    result = tracking._supabase_client.from_("sessions").select("*").eq("id", session_id).execute()
    print(f"✅ Session read back: {result.data[0]['streamlit_session_id']}")

    print("\n✅ All Supabase tests passed")
    return True


def test_langfuse():
    print("\n--- Testing Langfuse ---")
    from langfuse import get_client
    lf = get_client()
    if lf:
        print(f"✅ Langfuse client initialized")
    else:
        print("❌ Langfuse client failed — check LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST in .env")
        return False

    # Test a traced function
    from langfuse import observe

    @observe()
    def test_traced_function(x):
        return x * 2

    result = test_traced_function(21)
    print(f"✅ Traced function returned: {result}")

    # Flush to make sure data is sent
    lf.flush()
    print("✅ Langfuse data flushed — check your dashboard at https://cloud.langfuse.com")
    print("\n✅ All Langfuse tests passed")
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("v0.4 Observability Connection Test")
    print("=" * 50)

    supabase_ok = test_supabase()
    langfuse_ok = test_langfuse()

    print("\n" + "=" * 50)
    print(f"Supabase: {'✅ PASS' if supabase_ok else '❌ FAIL'}")
    print(f"Langfuse: {'✅ PASS' if langfuse_ok else '❌ FAIL'}")
    print("=" * 50)

    if supabase_ok:
        print("\nCheck Supabase: Dashboard → Table Editor → sessions/analysis_runs/user_events/reports")
    if langfuse_ok:
        print("Check Langfuse: https://cloud.langfuse.com → your project → Traces")
