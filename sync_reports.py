"""
Sync reports from Supabase to local reports/ folder.

Pulls cloud-generated reports that aren't already saved locally,
writes them as markdown files, and appends missing entries to test-log.csv.

Usage:
    python sync_reports.py           # sync all missing reports
    python sync_reports.py --list    # list remote reports without downloading
"""

import os
import sys
import csv
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
TEST_LOG_PATH = os.path.join(REPORTS_DIR, "test-log.csv")

LOCAL_TIME_FMT = "%Y-%m-%d %H:%M:%S"


def _utc_to_local(iso_str: str) -> str:
    """Convert an ISO 8601 UTC timestamp to local time, formatted to match agent.py output."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is not None:
            dt = dt.astimezone(tz=None)  # convert to system local timezone
        return dt.strftime(LOCAL_TIME_FMT)
    except (ValueError, TypeError):
        return iso_str


def _get_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("❌ SUPABASE_URL and SUPABASE_KEY must be set in .env")
        sys.exit(1)

    from postgrest import SyncPostgrestClient
    return SyncPostgrestClient(
        f"{url}/rest/v1",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )


def _get_local_report_filenames() -> set[str]:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    return {f for f in os.listdir(REPORTS_DIR) if f.endswith(".md")}


def _get_logged_filenames() -> set[str]:
    if not os.path.exists(TEST_LOG_PATH):
        return set()
    with open(TEST_LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["report_file"] for row in reader if "report_file" in row}


def fetch_remote_reports(client) -> list[dict]:
    """Fetch all reports joined with their analysis_run metadata."""
    reports = client.from_("reports").select("*").execute().data

    if not reports:
        return []

    run_ids = list({r["run_id"] for r in reports})
    runs = client.from_("analysis_runs").select("*").in_("id", run_ids).execute().data
    runs_by_id = {r["id"]: r for r in runs}

    enriched = []
    for report in reports:
        run = runs_by_id.get(report["run_id"], {})
        enriched.append({
            "report_filename": report["report_filename"],
            "report_markdown": report["report_markdown"],
            "search_queries": json.loads(report["search_queries"]) if isinstance(report["search_queries"], str) else report["search_queries"],
            "created_at": report["created_at"],
            "run_id": report["run_id"],
            "use_case": run.get("use_case", ""),
            "technology": run.get("technology", ""),
            "industry": run.get("industry", ""),
            "app_version": run.get("app_version", ""),
            "scenario_source": run.get("scenario_source", "custom"),
            "planning_sec": run.get("planning_sec"),
            "research_sec": run.get("research_sec"),
            "analysis_sec": run.get("analysis_sec"),
            "total_sec": run.get("total_sec"),
            "started_at": run.get("started_at"),
            "completed_at": run.get("completed_at"),
        })

    return enriched


def save_report_locally(report: dict) -> str:
    """Write a report markdown file to reports/. Returns the filepath."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filepath = os.path.join(REPORTS_DIR, report["report_filename"])

    run_id_line = f"**Run ID:** `{report['run_id']}`  \n" if report.get("run_id") else ""

    header = (
        f"# Compliance Gap Analysis Report\n\n"
        f"**Version:** {report['app_version']}  \n"
        f"{run_id_line}"
        f"**Use Case:** {report['use_case']}  \n"
        f"**Technology:** {report['technology']}  \n"
        f"**Industry:** {report['industry']}  \n"
        f"**Generated:** {_utc_to_local(report['created_at'])}  \n"
        f"**Source:** Synced from Supabase (cloud session)  \n"
    )

    timing = report.get("total_sec")
    if timing:
        header += (
            f"**Generation Time:** {report['total_sec']}s total "
            f"(planning: {report['planning_sec']}s, "
            f"research: {report['research_sec']}s, "
            f"analysis: {report['analysis_sec']}s)  \n"
        )

    header += f"\n---\n\n## Search Queries Used\n\n"
    queries_section = "\n".join(f"- {q}" for q in report["search_queries"]) + "\n\n"
    body = f"---\n\n## Analysis\n\n{report['report_markdown']}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + queries_section + body)

    return filepath


_TEST_LOG_FIELDS = [
    "timestamp", "version", "run_id", "use_case", "technology", "industry",
    "num_queries", "planning_sec", "research_sec", "analysis_sec", "total_sec",
    "report_file",
]


def append_to_test_log(report: dict) -> None:
    """Append a row to test-log.csv for a synced report."""
    raw_ts = report.get("completed_at") or report["created_at"]
    row = {
        "timestamp": _utc_to_local(raw_ts),
        "version": report["app_version"],
        "run_id": report.get("run_id", ""),
        "use_case": report["use_case"],
        "technology": report["technology"],
        "industry": report["industry"],
        "num_queries": len(report["search_queries"]),
        "planning_sec": report.get("planning_sec", ""),
        "research_sec": report.get("research_sec", ""),
        "analysis_sec": report.get("analysis_sec", ""),
        "total_sec": report.get("total_sec", ""),
        "report_file": report["report_filename"],
    }

    if os.path.exists(TEST_LOG_PATH):
        with open(TEST_LOG_PATH, "r", encoding="utf-8") as f:
            existing_header = f.readline().strip().split(",")
        if "run_id" not in existing_header:
            _migrate_csv_header()

    file_exists = os.path.exists(TEST_LOG_PATH)

    with open(TEST_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_TEST_LOG_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def _migrate_csv_header() -> None:
    """One-time migration: add run_id column to existing test-log.csv."""
    with open(TEST_LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        old_rows = list(reader)

    with open(TEST_LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_TEST_LOG_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for old_row in old_rows:
            old_row.setdefault("run_id", "")
            writer.writerow(old_row)


def sync(list_only: bool = False):
    print("🔄 Connecting to Supabase…")
    client = _get_client()

    print("📥 Fetching remote reports…")
    remote_reports = fetch_remote_reports(client)
    print(f"   Found {len(remote_reports)} report(s) in Supabase")

    if not remote_reports:
        print("✅ No reports in Supabase. Nothing to sync.")
        return

    local_files = _get_local_report_filenames()
    logged_files = _get_logged_filenames()

    missing_locally = [r for r in remote_reports if r["report_filename"] not in local_files]

    if list_only:
        print(f"\n{'='*60}")
        print(f"Remote reports: {len(remote_reports)} | Local: {len(local_files)} | Missing locally: {len(missing_locally)}")
        print(f"{'='*60}")
        for r in remote_reports:
            status = "✅ synced" if r["report_filename"] in local_files else "❌ missing"
            print(f"  {status}  {r['report_filename']}")
            print(f"           {r['use_case']} | {r['industry']} | {r['total_sec']}s")
        return

    if not missing_locally:
        print("✅ All remote reports already synced locally.")
        return

    print(f"\n📂 Syncing {len(missing_locally)} new report(s)…")
    for report in missing_locally:
        filepath = save_report_locally(report)
        print(f"   ✅ {report['report_filename']}")

        if report["report_filename"] not in logged_files:
            append_to_test_log(report)
            print(f"      📊 Added to test-log.csv")

    print(f"\n✅ Sync complete. {len(missing_locally)} report(s) saved to reports/")


if __name__ == "__main__":
    list_only = "--list" in sys.argv
    sync(list_only=list_only)
