# AI Compliance Gap Analyzer

An intelligent AI agent that analyzes AI implementations for regulatory compliance gaps and risks.

> **Status:** v0.4 — Active development. [**Live Demo**](https://ai-compliance-gap-analyzer.streamlit.app/) available. CLI pipeline also supported.

## Overview

Helps organizations identify compliance risks when deploying AI systems. Given a use case, technology stack, and industry context, the agent autonomously:

1. **Plans research** - Determines relevant compliance frameworks and vendor policies to investigate
2. **Conducts research** - Searches the web for regulatory requirements and technical documentation
3. **Analyzes gaps** - Identifies discrepancies between requirements and current implementation
4. **Provides recommendations** - Generates actionable compliance advice
5. **Saves report** - Persists a version-tagged markdown report for audit trail

### How It Works

```
User Input (use_case, technology, industry)
    │
    ▼
plan_searches() ──► Claude generates 3-5 search queries
    │
    ▼
conduct_research() ──► Tavily executes each query (max 3 results each)
    │
    ▼
analyze_compliance() ──► Claude analyzes all findings
    │
    ▼
save_report() ──► Markdown file saved to reports/
    │
    ▼
append_test_log() ──► Row appended to reports/test-log.csv
```

## Example Analysis

**Input:**
- Use case: "AI-powered resume screening tool"
- Technology: "OpenAI GPT-4 API"
- Industry: "Enterprise HR (US-based)"

**Output:**
- **Risk Prioritization Matrix** — executive summary table with gap, risk level, regulatory impact, implementation difficulty, and priority ranking
- Applicable regulations (EEOC AI guidance, NYC Local Law 144)
- Identified risks (bias, data retention, transparency requirements)
- Compliance gaps (missing bias audit, no candidate disclosure)
- Actionable recommendations grouped by urgency (immediate, short-term, medium-term)

Sample reports are included in the repo — see [`reports/`](reports/) for analyses across HR, healthcare, fintech, education, and RegTech scenarios.

## Tech Stack

- **AI Orchestration:** Claude Sonnet 4.5 (Anthropic API) with Extended Thinking
- **Web Research:** Tavily API
- **AI Observability:** Langfuse (traces, thinking, tokens, cost)
- **Database:** Supabase (user tracking, report persistence)
- **Frontend:** Streamlit
- **Language:** Python 3.14
- **Architecture:** Multi-step agentic workflow

## Project Structure

```
ai-compliance-gap-analyzer/
├── agent.py              # Main orchestrator (pipeline + test scenarios + timing + Langfuse)
├── streamlit_app.py      # Streamlit web UI (user event tracking)
├── tracking.py           # Supabase tracking (sessions, runs, events, reports)
├── sync_reports.py       # Pull cloud reports from Supabase to local reports/
├── test_tracking.py      # Integration tests (Supabase, Langfuse, parent trace, run_id)
├── tools.py              # Tavily web search and result formatting
├── prompts.py            # AI prompts for planning and analysis (with reasoning)
├── supabase_schema.sql   # Database schema (run in Supabase SQL Editor)
├── requirements.txt      # Python dependencies
├── CHANGELOG.md          # Version history
├── .streamlit/
│   └── config.toml       # Streamlit theme (dark mode)
├── reports/              # Generated compliance analysis reports
│   ├── report_v*.md      # Version-tagged markdown reports
│   └── test-log.csv      # Centralized performance log (local backup)
├── docs/                 # Project documentation
│   ├── DOCUMENTATION-GUIDE.md   # Documentation conventions
│   ├── iterations/              # One file per version — full analysis story
│   └── dev-logs/                # Session summaries
└── .env                  # API keys (not committed)
```

## Installation

```bash
# Clone repository
git clone https://github.com/yeyfreya/ai-compliance-gap-analyzer.git
cd ai-compliance-gap-analyzer

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY = <your-anthropic-key>
TAVILY_API_KEY   = <your-tavily-key>
```

## Usage

**Try the live demo:** [ai-compliance-gap-analyzer.streamlit.app](https://ai-compliance-gap-analyzer.streamlit.app/)

**Or run locally:**

```bash
python -m streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`. Pick a preset scenario or enter custom inputs, then click **Run Analysis**.

**Or run from CLI:**

```bash
python agent.py <scenario>
```

Available scenarios: `hr`, `healthcare`, `fintech`, `education`, `regtech`

```bash
python agent.py hr          # AI resume screening — US employment law
python agent.py healthcare  # AI diagnostics — HIPAA, FDA
python agent.py fintech     # AI credit scoring — UK FCA, GDPR
python agent.py education   # AI essay grading — FERPA, COPPA
python agent.py regtech     # AI compliance analyzer — RegTech SaaS
```

Each run generates a timestamped report in `reports/` and appends performance data to `reports/test-log.csv`.

## Known Issues (v0.4)

- Analysis usually takes 2–3 minutes but can exceed 5 minutes for complex or region-specific cases
- Report detail sections vary between runs (Risk Prioritization Matrix is fixed; rest is flexible)
- Linear pipeline only (no research adequacy validation loop yet)
- Supabase RLS disabled (acceptable for portfolio project; needs RLS for production)
- Streamlit Cloud deployment needs re-deploy after v0.4 Session 2 changes

All critical/high bugs from v0.1–v0.2 have been fixed.
See [v0.4 iteration doc](docs/iterations/v0.4-supabase-langfuse-tracking.md) for full details.

## Roadmap

- [x] Core agent logic
- [x] Autonomous research planning
- [x] Multi-source web search
- [x] Compliance gap analysis
- [x] Report persistence with version tagging
- [x] Bug fixes (data loss, truncation, error handling)
- [x] Input validation
- [x] Test scenario runner with CLI
- [x] Per-step timing and AI observability logging
- [x] Streamlit web interface
- [x] Risk Prioritization Matrix (mandatory first section)
- [x] Usage tracking & report persistence (Supabase)
- [x] AI agent observability (Langfuse — traces, extended thinking, tokens, cost)
- [x] Extended Thinking (Claude's internal reasoning captured and logged)
- [x] Cross-service correlation (`run_id` links local reports ↔ Supabase ↔ Langfuse)
- [x] Cloud report sync (`sync_reports.py` pulls Supabase reports to local)
- [ ] Consistent detailed report structure (full template enforcement)
- [ ] Pipeline → agent loop (research adequacy check)
- [ ] PDF report generation
- [x] Cloud deployment (Streamlit Cloud)
- [ ] OpenClaw plugin version (v2)

## Development

See [CHANGELOG.md](CHANGELOG.md) for version history and [docs/iterations/](docs/iterations/) for detailed analysis per version.

**Current version:** v0.4 — Supabase + Langfuse Tracking ([full iteration doc](docs/iterations/v0.4-supabase-langfuse-tracking.md))

## License

MIT

## Author

Freya Ye Yu - [LinkedIn](https://www.linkedin.com/in/yeyufreya/) - [Portfolio](https://www.yeyufreya.com/)
