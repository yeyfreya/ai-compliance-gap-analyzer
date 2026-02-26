# Changelog — AI Compliance Gap Analyzer

All notable changes to this project are documented here.
Each version represents an iteration, including what was analyzed, what changed, and why.

---

## [v0.2] - 2026-02-26 — Bug Fixes, Hardening & Observability

### Summary
Fixed all critical/high bugs from v0.1 baseline. Added test scenario runner, per-step
timing, and centralized performance logging — the project's first AI observability layer.
Tested across 4 diverse regulatory scenarios (HR, Healthcare, Fintech, Education).

### What Changed — Bug Fixes (Session 1)
- **Bug #1 fixed:** `format_search_results()` in `tools.py` — function received a list but treated it as a dict, causing all research data to be silently dropped. Now iterates the list directly.
- **Bug #2 closed:** Indentation inconsistency in `run_analysis()` — already fixed in prior session.
- **Bug #15 fixed:** `max_tokens` in `analyze_compliance()` increased from 3000 to 8000 — v0.1 test run confirmed analysis was truncating mid-table.
- **Bug #3 fixed:** Added `anthropic.APIError` handling to both Claude API calls in `agent.py` — pipeline degrades gracefully instead of crashing on API failures.
- **Bug #4 fixed:** Input validation on `run_analysis()` — rejects empty/whitespace/overlength inputs with error dict before any API calls are made.
- **Bug #6 closed:** Bare `except` in `plan_searches()` — already fixed in prior session (catches specific exceptions).

### What Changed — Test & Observability (Session 2)
- **Test scenarios:** Added `TEST_SCENARIOS` dict with 4 scenarios + CLI runner (`python agent.py <scenario>`)
- **Timing:** Per-step timing (planning, research, analysis) in `run_analysis()`, displayed in console output and report header
- **Test log:** New `append_test_log()` writes to `reports/test-log.csv` after every run — centralized performance tracking across versions
- **Test results:** All 4 scenarios passed. Analysis phase is the bottleneck (75-85% of total time). Report length varies 266-790 lines by regulatory complexity.

### What Changed — Docs, README & Rename (Session 3)
- **Documentation system:** Added README update rules (Section 7) to DOCUMENTATION-GUIDE.md with trigger table and workflow integration
- **Cursor rules synced:** Fixed dev log naming format (added HHMM), added commit message suggestion step
- **Documentation map:** Created local-only `docs/DOCUMENTATION-SYSTEM-MAP.md` — visual reference for the full documentation system
- **README updated to v0.2:** Status, architecture diagram, project structure, usage (CLI scenarios), known issues, roadmap, current version
- **Repo renamed:** `compliance-gap-analyzer` → `ai-compliance-gap-analyzer`; all current-state references updated

### New Issues Found
- #16: Analysis prompt doesn't enforce consistent report structure (Medium)
- #17: Windows GBK encoding error on emoji output (Medium)

Full details: [docs/iterations/v0.2-bug-fixes-and-observability.md](docs/iterations/v0.2-bug-fixes-and-observability.md)

---

## [v0.1] - 2026-02-25 — Baseline

### Summary
First working version of the AI Compliance Gap Analyzer. Three-stage pipeline
that plans searches, executes web research via Tavily, and sends findings to
Claude for structured compliance analysis.

### Architecture
- **agent.py** — Main orchestrator with 5 functions:
  `plan_searches()` → `conduct_research()` → `analyze_compliance()` → `save_report()` → `run_analysis()`
- **tools.py** — Web search via Tavily API with result formatting
- **prompts.py** — System prompt, search planning prompt, and analysis prompt
- **test_all.py / test_api.py / test_tavily.py** — Manual integration tests

### What Works
- End-to-end pipeline: user provides (use_case, technology, industry) → gets compliance gap report
- Claude plans 3-5 search queries dynamically
- Tavily executes advanced web searches
- Claude analyzes findings and produces structured report
- Reports saved as timestamped markdown files

### Analysis (14 findings from "Improve & Debug" chat)
- 2 bugs found (format_search_results type mismatch, indentation)
- 4 missing features (error handling, input validation, retry logic, specific exceptions)
- 2 architecture observations (linear pipeline not agent, stateless Claude calls)
- 2 prompt issues (misleading system prompt, generic analysis prompt)
- 2 code quality items (no version pins, unused streamlit dependency)
- 2 output quality items (raw research text, no sources in report)

Full details: [docs/iterations/v0.1-baseline.md](docs/iterations/v0.1-baseline.md)
