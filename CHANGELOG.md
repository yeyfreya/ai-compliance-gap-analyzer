# Changelog — AI Compliance Gap Analyzer

All notable changes to this project are documented here.
Each version represents an iteration, including what was analyzed, what changed, and why.

---

## [v0.2] - 2026-02-26 — Bug Fixes & Hardening

### Summary
Fix all remaining issues from v0.1 baseline analysis: live bugs, missing error
handling, prompt improvements, and dependency hygiene.

### What Changed
- **Bug #1 fixed:** `format_search_results()` in `tools.py` — function received a list but treated it as a dict, causing all research data to be silently dropped. Now iterates the list directly.
- **Bug #2 closed:** Indentation inconsistency in `run_analysis()` — already fixed in prior session.
- **Bug #15 fixed:** `max_tokens` in `analyze_compliance()` increased from 3000 to 8000 — v0.1 test run confirmed analysis was truncating mid-table.
- **Bug #3 fixed:** Added `anthropic.APIError` handling to both Claude API calls in `agent.py` — pipeline degrades gracefully instead of crashing on API failures.
- **Bug #4 fixed:** Input validation on `run_analysis()` — rejects empty/whitespace/overlength inputs with error dict before any API calls are made.
- **Bug #6 closed:** Bare `except` in `plan_searches()` — already fixed in prior session (catches specific exceptions).

Full details: [docs/iterations/v0.2-bug-fixes.md](docs/iterations/v0.2-bug-fixes.md)

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
