# Changelog — AI Compliance Gap Analyzer

All notable changes to this project are documented here.
Each version represents an iteration, including what was analyzed, what changed, and why.

---

## [v0.1] - 2026-02-25 — Baseline

### Summary
First working version of the AI Compliance Gap Analyzer. This is the foundational
architecture: a three-stage pipeline that plans searches, executes web research via
Tavily, and sends findings to Claude for structured compliance analysis.

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
- Claude analyzes findings and produces structured report (regulations, risks, gaps, recommendations)
- Reports saved as timestamped markdown files

### Known Limitations (to address in future versions)
- No error handling around Claude API calls (only Tavily has try/except)
- `format_search_results()` signature mismatch — expects list but receives dict
- No input validation on user parameters
- No streaming or progress feedback beyond print statements
- No UI yet (Streamlit listed in requirements but not implemented)
- Prompts are functional but could be more structured for consistent output
