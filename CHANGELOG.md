# Changelog — AI Compliance Gap Analyzer

All notable changes to this project are documented here.
Each version represents an iteration, including what was analyzed, what changed, and why.

---

## [v0.4] - 2026-02-27 — Supabase + Langfuse Tracking

### Summary
Set up comprehensive observability: Langfuse for AI agent tracing (extended thinking,
token usage, cost, per-step reasoning) and Supabase for user behavior tracking (sessions,
events, report persistence). Extended Thinking enabled on both Claude calls. Structured
reasoning prompts added so Claude explains its decision-making in every report.

### What Changed — Session 1: Observability Setup (2026-02-27)
- **Extended Thinking** (`agent.py`): Enabled on `plan_searches()` (3k budget) and `analyze_compliance()` (8k budget). Both now return dicts with thinking text, token counts
- **Langfuse instrumentation** (`agent.py`): `@observe()` decorators on all pipeline functions + `AnthropicInstrumentor` for automatic Claude API tracing
- **Structured reasoning** (`prompts.py`): Planning prompt asks for query rationale; analysis prompt adds "Agent Reasoning" section to every report
- **Supabase tracking** (`tracking.py`): New module — fail-safe session/run/event/report tracking via PostgREST
- **Schema** (`supabase_schema.sql`): 4 tables (sessions, analysis_runs, user_events, reports)
- **Streamlit updates** (`streamlit_app.py`): User event tracking, Supabase/Langfuse secrets injection, handles new dict return types
- **Dependencies** (`requirements.txt`): Added `postgrest`, `langfuse>=4.0.0b1`, `opentelemetry-instrumentation-anthropic`
- **Cursor rule** (`.cursor/rules/no-assumptions.mdc`): AI agent must confirm assumptions with user before acting

### What Changed — Session 2: Architecture Fix, Correlation, UI Polish & Report Sync (2026-02-28)
- **Parent Langfuse trace** (`streamlit_app.py`): Extracted pipeline into `@observe(name="compliance_pipeline")` wrapper — all three steps now group under one parent trace instead of creating separate fragmented traces. Tagged with `run_id`/`session_id` via OTel span attributes
- **Universal correlation key** (`agent.py`, `streamlit_app.py`, `sync_reports.py`): Supabase `run_id` embedded in local report headers, test-log.csv, Langfuse trace metadata, and synced reports — single key to navigate between all systems
- **Product identity** (`streamlit_app.py`): Removed "Claude" name-drops from pipeline step messages — the agent presents as the product
- **Time expectations** (`streamlit_app.py`): Timer subtitle now says "Usually 2–3 min · may take longer for complex or region-specific cases"
- **Report sync** (`sync_reports.py`): New CLI script pulls cloud-generated reports from Supabase to local `reports/` with UTC→local timestamp conversion. Idempotent
- **Agent rules consolidated** (`.cursor/rules/agent-behavior.mdc`): Combined no-assumptions, root-cause surfacing, and product marketing thinking into one rule. Deleted standalone `no-assumptions.mdc`
- **CSV column migration** (`agent.py`, `sync_reports.py`): `run_id` column added to test-log.csv with automatic one-time header migration for existing CSVs
- **Integration tests** (`test_tracking.py`): Expanded from basic connection test to 4-part test suite: Supabase cross-table linkage, Langfuse connection, parent trace architecture (nested spans + metadata), local report correlation (run_id in report header + CSV)
- **Known non-bug rule** (`.cursor/rules/documentation-system.mdc`): Documented Windows GBK emoji error as Cursor shell bug — agents must not strip emoji from code

### What Changed — Session 3: Branching (2026-02-28)
- **Branching guide** (`docs/BRANCHING-GUIDE.md`): main/dev workflow, PR-based merges, release tagging, optional staging app for Streamlit Cloud testing
- **Docs updated**: DOCUMENTATION-GUIDE workflow, README project structure and Development section

Full details: [docs/iterations/v0.4-supabase-langfuse-tracking.md](docs/iterations/v0.4-supabase-langfuse-tracking.md)

---

## [v0.3] - 2026-02-26 — Streamlit UI & Report Structure

### Summary
Built a Streamlit web interface for live demo — users can input their AI scenario and
receive a full compliance gap report through a polished UI. Added mandatory Risk
Prioritization Matrix as the first section of every report.

### What Changed — Session 1: UI & Report Structure
- **Streamlit app** (`streamlit_app.py`): Full web UI with sidebar scenario picker, step-by-step progress tracking, live JS elapsed timer, timing metrics cards, tabbed report/queries view, and markdown download button
- **Theme** (`.streamlit/config.toml`): Dark theme with blue primary color
- **Analysis prompt rewrite** (`prompts.py`): Risk Prioritization Matrix enforced as first section; standardized risk levels (CRITICAL/HIGH/MEDIUM/LOW); flexible structure for detailed analysis sections
- **Bug #17 closed** (`agent.py`): Windows GBK encoding error investigated — only occurs in Cursor's shell runner, not in user's own terminal. Not a code bug; no fix applied
- **New test scenario** (`agent.py`): `regtech` — the tool analyzing itself (RegTech / AI compliance SaaS)
- **Timer UX**: Live JS clock counts during analysis, stops on completion with static "Report generated in X:XX"

### What Changed — Session 2: Cloud Deployment - 2026-02-27
- **Streamlit Cloud secrets** (`streamlit_app.py`): Injects `st.secrets` as env vars before agent import; clear error message if secrets are missing
- **Pinned requirements** (`requirements.txt`): Added `>=` floor versions for all dependencies
- **Deployed to Streamlit Cloud**: Live public demo connected to GitHub repo

### Test Results
- 4 Streamlit test runs: regtech (x2), documentation tool, HR — all passed
- Analysis time: 48s–185s depending on regulatory complexity and report length
- Reports: 289–789 lines with structured prompt

Full details: [docs/iterations/v0.3-streamlit-ui.md](docs/iterations/v0.3-streamlit-ui.md)

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
