# Documentation Guide — AI Compliance Gap Analyzer

This file defines how all documentation is structured, named, and maintained in this project.
Any AI agent working on this project should follow these conventions exactly.

---

## Project Structure

```
compliance-gap-analyzer/
├── agent.py                  # Main orchestrator
├── tools.py                  # Search tools (Tavily)
├── prompts.py                # Prompts sent to Claude
├── requirements.txt          # Python dependencies
├── CHANGELOG.md              # Version history (summary per version)
├── .gitignore                # Protects .env, .cursor/, transcripts, etc.
│
├── .cursor/rules/            # Cursor rules (committed to git)
│   ├── documentation-system.mdc   # Auto-read docs before working
│   └── pre-commit-review.mdc      # Pre-commit checklist for agents
│
├── reports/                  # Generated compliance analysis reports
│   └── report_v<VERSION>_<use-case-slug>_<YYYYMMDD_HHMMSS>.md
│
└── docs/
    ├── DOCUMENTATION-GUIDE.md    # THIS FILE — how to document everything
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

Examples: `v0.1-baseline.md`, `v0.2-bug-fixes.md`, `v0.3-prompt-improvements.md`

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

## 4. Dev Logs (`docs/dev-logs/`)

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

## 5. Chat Transcripts (`docs/dev-logs/transcripts/`)

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

## 6. Git Commit Messages

### Format
`v<VERSION>: Short description of what changed`

Examples:
- `v0.1: Baseline - initial working compliance gap analyzer`
- `v0.1: Add dev logs, version-tagged reports, and documentation system`
- `v0.2: Fix format_search_results bug and add error handling`

### Rules
- One commit per logical change or per work session
- The commit message describes the "what" — the iteration doc and dev log describe the "why"

---

## Version Management

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

## Workflow for Each New Version

1. Review the previous version's "Remaining Issues" section
2. Create `docs/iterations/v0.X-description.md` with Goal section
3. Make code changes — update the iteration doc as you go
4. Run tests — add Test Results to the iteration doc
5. Update CHANGELOG.md with version summary
6. Write dev log summary for the chat session
7. User exports chat transcript from Cursor
8. Commit and push:
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
4. Follow all naming conventions and file structures above
5. At the end of the session, write a dev log summary in `docs/dev-logs/`
6. Update the iteration doc with any new findings or test results
