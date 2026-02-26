# AI Compliance Gap Analyzer

An intelligent AI agent that analyzes AI implementations for regulatory compliance gaps and risks.

> **Status:** v0.1 — Active development. Command-line pipeline working, web interface planned.

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

A sample report is included in the repo: [`reports/report_v0.1_ai-powered-resume-screening-tool_20260225_155951.md`](reports/report_v0.1_ai-powered-resume-screening-tool_20260225_155951.md)

## Tech Stack

- **AI Orchestration:** Claude Sonnet 4.5 (Anthropic API)
- **Web Research:** Tavily API
- **Language:** Python 3.14
- **Architecture:** Multi-step agentic workflow

## Project Structure

```
compliance-gap-analyzer/
├── agent.py              # Main orchestrator (plan → research → analyze → report)
├── tools.py              # Tavily web search and result formatting
├── prompts.py            # AI prompts for planning and analysis
├── test_all.py           # Combined import + API integration test
├── test_api.py           # Claude API connection test
├── test_tavily.py        # Tavily search test
├── requirements.txt      # Python dependencies
├── CHANGELOG.md          # Version history
├── reports/              # Generated compliance analysis reports (tracked in git)
├── docs/                 # Project documentation
│   ├── DOCUMENTATION-GUIDE.md   # Documentation conventions
│   ├── iterations/              # One file per version — full analysis story
│   └── dev-logs/                # Session summaries
└── .env                  # API keys (not committed)
```

## Installation

```bash
# Clone repository
git clone https://github.com/yeyfreya/compliance-gap-analyzer.git
cd compliance-gap-analyzer

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

**Command-line (current):**

```bash
python agent.py
```

Edit the test scenario at the bottom of `agent.py` to analyze different use cases.

**Web interface (coming soon):**

Streamlit UI in development.

## Known Issues (v0.1)

- `format_search_results` has a type mismatch bug — research data may be dropped
- Analysis output can be truncated when Claude produces long responses (`max_tokens` too low)
- No error handling on API calls — failures crash the pipeline
- Linear pipeline only (no research adequacy validation loop yet)

See [v0.1 baseline analysis](docs/iterations/v0.1-baseline.md) for the full list of 14 findings.

## Roadmap

- [x] Core agent logic
- [x] Autonomous research planning
- [x] Multi-source web search
- [x] Compliance gap analysis
- [x] Report persistence with version tagging
- [ ] Bug fixes (format_search_results type mismatch, max_tokens truncation)
- [ ] Error handling & input validation
- [ ] Richer analysis output (severity ratings, compliance scores)
- [ ] Pipeline → agent loop (research adequacy check)
- [ ] Streamlit web interface
- [ ] PDF report generation
- [ ] Cloud deployment
- [ ] OpenClaw plugin version (v2)

## Development

See [CHANGELOG.md](CHANGELOG.md) for version history and [docs/iterations/](docs/iterations/) for detailed analysis per version.

**Current version:** v0.1 — Baseline ([full iteration doc](docs/iterations/v0.1-baseline.md))

## License

MIT

## Author

Freya Ye Yu - [LinkedIn](https://www.linkedin.com/in/yeyufreya/) - [Portfolio](https://www.yeyufreya.com/)
