# Documentation Guide — AI Compliance Gap Analyzer

This file defines how all documentation is structured, named, and maintained in this project.
Any AI agent working on this project should follow these conventions exactly.

---

## Project Structure

```
ai-compliance-gap-analyzer/
├── agent.py                  # Main orchestrator (pipeline + test scenarios + timing)
├── tools.py                  # Search tools (Tavily)
├── prompts.py                # Prompts sent to Claude
├── requirements.txt          # Python dependencies
├── CHANGELOG.md              # Version history (summary per version)
├── .gitignore                # Protects .env, .cursor/, transcripts, etc.
│
├── .cursor/rules/            # Cursor rules (committed to git)
│   ├── documentation-system.mdc   # Auto-read docs before working
│   ├── no-assumptions.mdc         # Confirm before interpreting user intent
│   └── pre-commit-review.mdc      # Pre-commit checklist for agents
│
├── reports/                  # Generated compliance analysis reports
│   ├── report_v<VERSION>_<use-case-slug>_<YYYYMMDD_HHMMSS>.md
│   └── test-log.csv          # Centralized performance log (AI observability)
│
└── docs/
    ├── DOCUMENTATION-GUIDE.md    # THIS FILE — how to document everything
    ├── PROJECT-SCHEMA.md         # LOCAL ONLY — project vision, strategy, sourced quotes
    │
    ├── iterations/               # One file per version — the full story
    │   └── v<VERSION>-<short-description>.md
    │
    └── dev-logs/                 # Chat session summaries
        ├── v<VERSION>_<YYYY-MM-DD>_<HHMM>_<short-topic>.md
        │
        └── transcripts/         # LOCAL ONLY — not tracked in git
            └── export_v<VERSION>_<YYYY-MM-DD>_<HHMM>_<short-topic>.md
```

---

## 1. Version Iteration Docs (`docs/iterations/`)

**One file per version.** Each file tells the complete story of that version.

### Naming
`v<MAJOR>.<MINOR>-<short-description>.md`

Examples: `v0.1-baseline.md`, `v0.2-bug-fixes-and-observability.md`, `v0.3-prompt-improvements.md`

### Sections (in order)

```markdown
# v0.X — Short Description

## Project Snapshot
- Files table (file, purpose, line count)
- Architecture flow diagram

## Changes Made During This Version
- What code was added/modified and why

## Code Analysis
- Strengths
- Bugs found (with file, line, description, impact)
- Missing features
- Architecture observations
- Prompt quality issues
- Code quality items

## Test Results
- What was tested (use case, parameters)
- What worked
- What failed / issues observed
- Link to the generated report file

## Remaining Issues for v0.X+1
- Consolidated table: issue #, description, category, priority, source
- Source = "Code analysis" or "Test run"

## Version Log
- Timeline of key events during this version
```

### Rules
- Do NOT split into multiple files per version (no separate test-notes or baseline files)
- Update the file as you work through the version — it grows over time
- The "Remaining Issues" section becomes the roadmap for the next version
- **Title must stay accurate across sessions.** If a version spans multiple chat sessions that expand the scope beyond the original title, update the `# v0.X — Short Description` heading (and the filename if needed) to reflect the full scope. Example: `v0.2-bug-fixes.md` became `v0.2-bug-fixes-and-observability.md` after a second session added timing and test logging. Also update any references in `CHANGELOG.md` and dev logs.

---

## 2. CHANGELOG.md (Root)

**Short summary per version.** Points to the detailed iteration doc.

### Format

```markdown
## [v0.X] - YYYY-MM-DD — Short Title

### Summary
1-3 sentences describing what this version is about.

### Architecture
Key files and their roles.

### What Works / What Changed
Bullet points.

### Analysis
Summary counts (e.g., "14 findings: 2 bugs, 4 missing features...")

Full details: [docs/iterations/v0.X-description.md](docs/iterations/v0.X-description.md)
```

---

## 3. Reports (`reports/`)

**Generated output from running agent.py.** These are tracked in git.

### Naming
`report_v<VERSION>_<use-case-slug>_<YYYYMMDD_HHMMSS>.md`

Example: `report_v0.1_ai-powered-resume-screening-tool_20260225_155951.md`

### How they're created
- `save_report()` in `agent.py` generates these automatically
- The `version` parameter is passed through `run_analysis()`
- When bumping versions, update the default version string in code

### Rules
- Never delete old reports — they document what each code version produced
- Reports are tracked in git (not in .gitignore)

---

## 4. AI Observability (`reports/test-log.csv`)

**Centralized performance tracking across all runs and versions.**

This is the project's lightweight AI observability layer — tracking how the agent performs
over time so we can monitor latency, spot regressions, and make data-driven product decisions.

### What Gets Logged

Every successful `run_analysis()` call appends one row to `reports/test-log.csv` with:

| Column | Description |
|---|---|
| `timestamp` | When the run completed |
| `version` | Code version (e.g., `v0.2`) |
| `use_case` | Input: what the AI system does |
| `technology` | Input: technology being used |
| `industry` | Input: industry context |
| `num_queries` | How many search queries Claude planned |
| `planning_sec` | Time for Claude to plan searches |
| `research_sec` | Time for Tavily to execute all searches |
| `analysis_sec` | Time for Claude to write the analysis |
| `total_sec` | End-to-end pipeline time |
| `report_file` | Filename of the generated report |

### How It Works

- `run_analysis()` in `agent.py` wraps each pipeline step with `time.time()` calls
- Timing is included in the result dict under `result['timing']`
- `save_report()` writes timing into the report header
- `append_test_log()` appends a row to the CSV after every run

### Rules
- The CSV is append-only — never delete rows (they're your historical record)
- The CSV is tracked in git alongside reports
- When bumping versions, timing data naturally segments by the `version` column

### Future Growth

This is the starting point. As the project matures, consider:
- **Cost tracking** — log token usage and estimated API costs per run
- **Output quality metrics** — report length, number of gaps found, number of recommendations
- **Error tracking** — log failed runs with error type and which step failed
- **Dedicated tooling** — migrate to Langfuse, LangSmith, or similar when dashboard/alerting needs arise

---

## 5. Dev Logs (`docs/dev-logs/`)

**One summary per chat session.** Documents questions asked, answers given, and decisions made.

### Naming
`v<VERSION>_<YYYY-MM-DD>_<HHMM>_<short-topic>.md`

`HHMM` is the approximate session start time (24-hour format) to distinguish multiple sessions on the same day.

Example: `v0.1_2026-02-25_1711_improve-and-debug.md`

### Sections

```markdown
# Dev Log: Short Topic Title

**Version:** v0.X
**Date:** YYYY-MM-DD

## What Happened in This Session

### Task 1: Title
**Question:** What the user asked
**Answer/Solution:** What was done
**Decision:** What was decided and why
**Files modified:** List of files changed and where what changed

(repeat for each task)

## Key Decisions Made
- Numbered list of decisions

## Related Files
- Links to iteration docs, reports, transcripts
```

### Rules
- The agent writes the summary at the end of each session
- Keep it concise — capture the "what and why", not every word
- Link to related iteration docs and reports

---

## 6. Chat Transcripts (`docs/dev-logs/transcripts/`)

**Full exported chat logs — local only, not published to GitHub.**
The user exports these directly from Cursor. Remind user to do so.

### Naming
`export_v<VERSION>_<YYYY-MM-DD>_<HHMM>_<short-topic>.md`

Must match the corresponding dev log summary filename with `export_` prepended.

### Rules
- The user exports these from Cursor (not the agent)
- These are the raw record — no editing needed
- The summary file is what you read first; the transcript is for when you need exact wording
- **Not tracked in git** — listed in `.gitignore` to keep personal info (emails, local paths) private
- Kept locally for reference only

---

## 7. Project Schema (`docs/PROJECT-SCHEMA.md`)

**High-level overview of the project vision, strategy, and phased plan — local only, not tracked in git.**

This file summarizes the "big picture" by pulling sourced quotes directly from chat transcripts. It answers: what is this project, who is it for, what's the phased strategy, and what architectural decisions were made and why.

### What It Contains

- What the project is (industry, target users)
- The phased strategy (demo → temporary Streamlit → independent product or plugin)
- Key architectural decisions with sourced quotes
- Version history summary
- What's next (planned features)
- Source transcript table (which transcript said what)

### Rules
- **Local only** — listed in `.gitignore`. Contains sourced quotes from transcripts which may reference personal info.
- **Updated when the project vision, strategy, or direction changes** — not every session, only when the user makes a strategic decision (new product direction, new target user, new phase started, key architectural decision).
- **Every claim must have a source** — a direct quote and the transcript filename. Do not infer or assume; only document what the user actually said.
- **The agent should proactively update this file** when it detects a strategic decision in conversation (e.g., "I want to pivot to...", "my plan is to...", "I'm targeting...").

---

## 8. README.md (Root)

**The public-facing overview of the project.** Must stay accurate as the project evolves.

### What README.md Contains

- Project status line with current version
- Overview and architecture diagram
- Example analysis input/output
- Tech stack
- Project structure tree
- Installation and usage instructions
- Known Issues section (reflects current version)
- Roadmap with checked/unchecked items
- Current version line with link to iteration doc

### When to Update README.md

Update the README whenever any of these change:

| Trigger | What to Update in README |
|---|---|
| **New version started** | Status line (`v0.X`), "Current version" line at bottom, Known Issues section |
| **Bug fixed or feature added** | Known Issues (remove fixed items), Roadmap (check off completed items) |
| **New file added to project** | Project Structure tree |
| **Architecture changed** | Overview diagram, Tech stack if applicable |
| **New known issues found** | Known Issues section |
| **Repo renamed or clone URL changed** | Installation section (git clone URL) |

### Rules
- Keep the README concise — it's a landing page, not deep documentation
- Known Issues should reflect the **current** version only (not historical); link to the iteration doc for the full list
- Roadmap checkboxes should match actual project state
- The "Current version" line at the bottom must match the version in `agent.py`
- When in doubt, update it — a stale README is worse than a slightly verbose one

---

## 9. Git Commit Messages

### Format
`v<VERSION>: Short description of what changed`

Examples:
- `v0.1: Baseline - initial working compliance gap analyzer`
- `v0.1: Add dev logs, version-tagged reports, and documentation system`
- `v0.2: Fix format_search_results bug and add error handling`

### Rules
- One commit per logical change or per work session
- The commit message describes the "what" — the iteration doc and dev log describe the "why"
- **After completing documentation updates, the agent should suggest a commit message** following the format above. This is typically the last step before the user commits and pushes.

### Suggested Commit Message Template

After logging and updating all documentation, suggest a commit message like:

```
v<VERSION>: <what changed in code> + docs
```

Examples by session type:
- **Code changes only:** `v0.2: Fix format_search_results bug and add error handling`
- **Code + tests:** `v0.2: Add test scenarios, timing, and observability logging`
- **Docs only (mid-version):** `v0.2: Update iteration doc and changelog for session 2`
- **Full session (code + docs):** `v0.2: Add timing and test log + docs update`

If a session spans multiple concerns, summarize the biggest changes -- don't list everything. The iteration doc and dev log have the details.

---

## 10. Version Management

The current version is defined in one place in code: the `version` default parameter in `run_analysis()` inside `agent.py`.

### How to Bump the Version
When the user says "let's start v0.X", the agent should:
1. Update the default `version` parameter in `run_analysis()` in `agent.py`
2. Create a new iteration doc: `docs/iterations/v<NEW>-<description>.md`
3. Add a new entry to `CHANGELOG.md`

### Version Numbering
- `v0.1`, `v0.2`, `v0.3`... — incremental improvements
- Each version represents a batch of related changes (bug fixes, new feature, etc.)
- The user decides when to bump — the agent should ask if unsure

---

## 11. Workflow for Each New Version

1. Review the previous version's "Remaining Issues" section
2. Create `docs/iterations/v0.X-description.md` with Goal section
3. Make code changes — update the iteration doc as you go
4. Run tests — add Test Results to the iteration doc
5. Update CHANGELOG.md with version summary
6. Update README.md — version status, known issues, roadmap, structure (see Section 8)
7. Update `docs/PROJECT-SCHEMA.md` if any strategic decisions were made (see Section 7)
8. Write dev log summary for the chat session
9. User exports chat transcript from Cursor
10. Agent suggests a commit message (see Section 9)
11. Commit and push:
   ```powershell
   git add .
   git commit -m "v0.X: description"
   git push
   ```

---

## For AI Agents: Quick Reference

When starting a new chat on this project:
1. Read this file first
2. Read the latest `docs/iterations/v0.X-*.md` to understand current state
3. Read `CHANGELOG.md` for version history overview
4. Read `docs/PROJECT-SCHEMA.md` for the project vision and strategic direction
5. Follow all naming conventions and file structures above
6. At the end of the session, write a dev log summary in `docs/dev-logs/`
7. Update the iteration doc with any new findings or test results
8. Update `README.md` if version, known issues, roadmap, or project structure changed
9. Update `docs/PROJECT-SCHEMA.md` if any strategic decisions were made during the session
