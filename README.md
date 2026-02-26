# AI Compliance Gap Analyzer

An intelligent AI agent that analyzes AI implementations for regulatory compliance gaps and risks.

> **Status:** v0.2 — Active development. CLI pipeline working with test scenarios and timing. Web interface planned.

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
- Applicable regulations (EEOC AI guidance, NYC Local Law 144)
- Identified risks (bias, data retention, transparency requirements)
- Compliance gaps (missing bias audit, no candidate disclosure)
- Specific recommendations (implement bias testing, update disclosures)

Sample reports are included in the repo — see [`reports/`](reports/) for analyses across HR, healthcare, fintech, and education scenarios.

## Tech Stack

- **AI Orchestration:** Claude Sonnet 4.5 (Anthropic API)
- **Web Research:** Tavily API
- **Language:** Python 3.14
- **Architecture:** Multi-step agentic workflow

## Project Structure

```
ai-compliance-gap-analyzer/
├── agent.py              # Main orchestrator (pipeline + test scenarios + timing)
├── tools.py              # Tavily web search and result formatting
├── prompts.py            # AI prompts for planning and analysis
├── requirements.txt      # Python dependencies
├── CHANGELOG.md          # Version history
├── reports/              # Generated compliance analysis reports
│   ├── report_v*.md      # Version-tagged markdown reports
│   └── test-log.csv      # Centralized performance log (AI observability)
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

**Run a built-in test scenario:**

```bash
python agent.py <scenario>
```

Available scenarios: `hr`, `healthcare`, `fintech`, `education`

```bash
python agent.py hr          # AI resume screening — US employment law
python agent.py healthcare  # AI diagnostics — HIPAA, FDA
python agent.py fintech     # AI credit scoring — UK FCA, GDPR
python agent.py education   # AI essay grading — FERPA, COPPA
```

Each run generates a timestamped report in `reports/` and appends performance data to `reports/test-log.csv`.

**Web interface (coming soon):**

Streamlit UI in development.

## Known Issues (v0.2)

- Analysis prompt doesn't enforce consistent report structure — output format varies between runs
- Linear pipeline only (no research adequacy validation loop yet)

All critical/high bugs from v0.1 (data loss, truncation, missing error handling) have been fixed.
See [v0.2 iteration doc](docs/iterations/v0.2-bug-fixes-and-observability.md) for full details.

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
- [ ] Consistent report structure (prompt template enforcement)
- [ ] Richer analysis output (severity ratings, compliance scores)
- [ ] Pipeline → agent loop (research adequacy check)
- [ ] Streamlit web interface
- [ ] PDF report generation
- [ ] Cloud deployment
- [ ] OpenClaw plugin version (v2)

## Development

See [CHANGELOG.md](CHANGELOG.md) for version history and [docs/iterations/](docs/iterations/) for detailed analysis per version.

**Current version:** v0.2 — Bug Fixes, Hardening & Observability ([full iteration doc](docs/iterations/v0.2-bug-fixes-and-observability.md))

## License

MIT

## Author

Freya Ye Yu - [LinkedIn](https://www.linkedin.com/in/yeyufreya/) - [Portfolio](https://www.yeyufreya.com/)
