# Git Branching Guide — AI Compliance Gap Analyzer

A practical reference for the main/dev branching workflow.
Bookmark this file. Refer to it before every push, merge, or tag.

---

## Branch Roles

| Branch | Purpose | Who deploys from it | Push directly? |
|--------|---------|---------------------|----------------|
| `main` | Production — what users see on Streamlit Cloud | Streamlit Cloud (auto-deploy) | **Never** — merge via PR only |
| `dev`  | Working branch — local development, testing | Nobody — this is your workbench | Yes — commit and push freely |

**Rule:** Code flows one direction: `dev → main`. Never the reverse.

---

## One-Time Setup (Do This Once)

Run these commands in order from PowerShell in the project root:

```powershell
# 1. Make sure you're on main and it's clean
git checkout main
git status
# Should say "nothing to commit, working tree clean"

# 2. Tag the current production state
git tag v0.4

# 3. Push the tag to GitHub
git push origin v0.4

# 4. Create the dev branch from main
git checkout -b dev

# 5. Push dev to GitHub so it exists on remote
git push -u origin dev
```

After this, you'll have:
- `main` on GitHub = production (Streamlit Cloud deploys from this)
- `dev` on GitHub = your working branch
- `v0.4` tag = snapshot of production at the point you set up branching

---

## Daily Workflow (Working on `dev`)

### Starting work

```powershell
# Make sure you're on dev
git checkout dev

# Pull latest (in case you pushed from another machine)
git pull origin dev
```

### Committing your work

```powershell
# Stage and commit
git add .
git commit -m "v0.5: description of what changed"

# Push to remote
git push origin dev
```

### Checking which branch you're on

```powershell
git branch
# The asterisk (*) shows your current branch
```

---

## Merging to Production (dev → main via Pull Request)

Do this when you have a tested, stable version ready for users.

### Option A: Create PR from GitHub (Recommended)

```powershell
# 1. Make sure dev is pushed and up to date
git checkout dev
git push origin dev

# 2. Create the PR using GitHub CLI
gh pr create --base main --head dev --title "v0.5: Release description" --body "Summary of what's in this release"
```

Or go to GitHub → Pull Requests → New Pull Request → base: `main` ← compare: `dev`.

### Option B: Create PR from command line (if you don't have `gh` CLI)

Go to: `https://github.com/yeyfreya/ai-compliance-gap-analyzer/compare/main...dev`

Click "Create pull request", add a title and description, then merge.

### After merging the PR

```powershell
# 1. Switch to main and pull the merge
git checkout main
git pull origin main

# 2. Tag the release
git tag v0.5
git push origin v0.5

# 3. Switch back to dev for future work
git checkout dev

# 4. Sync dev with main (so dev has the merge commit)
git merge main
git push origin dev
```

---

## Tagging Releases

Tags create permanent snapshots on `main`. They show up on GitHub's Releases page.

```powershell
# Tag after merging to main
git checkout main
git tag v0.5
git push origin v0.5
```

### Viewing tags

```powershell
git tag            # List all tags
git show v0.4      # Show details of a specific tag
```

### Creating an annotated tag (with a message)

```powershell
git tag -a v0.5 -m "Streamlit UI polish, report sync, observability"
git push origin v0.5
```

---

## Quick Reference: Which Commands Are Safe Where

| Action | On `dev` | On `main` |
|--------|----------|-----------|
| `git add . && git commit` | Yes | **No** — merge via PR |
| `git push` | Yes | Only after PR merge + pull |
| `git pull` | Yes | Yes (to get merged changes) |
| `git tag` | No — tag on main only | Yes |
| `git merge main` | Yes (to sync after PR merge) | **No** — use PR |
| `git push --force` | **Avoid** | **Never** |
| `git reset --hard` | **Dangerous** — avoid | **Never** |

---

## Emergency: Fixing a Bug in Production

If you find a critical bug in the live app and need to fix it fast:

```powershell
# 1. Make sure main is up to date
git checkout main
git pull origin main

# 2. Create a hotfix branch from main
git checkout -b hotfix/fix-description

# 3. Make the fix, commit
git add .
git commit -m "v0.4.1: Fix critical bug description"

# 4. Push and create PR to main
git push -u origin hotfix/fix-description
gh pr create --base main --head hotfix/fix-description --title "Hotfix: description"

# 5. After PR is merged, tag and sync
git checkout main
git pull origin main
git tag v0.4.1
git push origin v0.4.1

# 6. Sync the fix into dev
git checkout dev
git merge main
git push origin dev

# 7. Delete the hotfix branch
git branch -d hotfix/fix-description
git push origin --delete hotfix/fix-description
```

This is the only time you'd create a branch other than `dev`.

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Accidentally committing on `main`

**Prevention:** Always run `git branch` before committing to check which branch you're on.

**Recovery if it happens (before pushing):**
```powershell
# Move the commit to dev instead
git checkout dev
git merge main
git checkout main
git reset --hard origin/main
```

### Mistake 2: Forgetting to sync `dev` after merging a PR

**What happens:** `dev` diverges from `main` because the merge commit only exists on `main`.

**Fix:**
```powershell
git checkout dev
git merge main
git push origin dev
```

### Mistake 3: Pushing directly to `main` instead of using a PR

**Prevention:** GitHub can enforce this — see "Branch Protection" below.

**Recovery:** The push already happened. Create the tag if it was intentional. If it was accidental, don't force-push to undo — just move forward.

### Mistake 4: Working on `main` by habit

**Fix your default:** After the one-time setup, always start your session with:
```powershell
git checkout dev
```

---

## Optional: Branch Protection on GitHub

To prevent accidental direct pushes to `main`:

1. Go to GitHub → Settings → Branches → Branch protection rules
2. Click "Add rule"
3. Branch name pattern: `main`
4. Check: "Require a pull request before merging"
5. Save changes

This makes it physically impossible to `git push` directly to `main`. You'll always need a PR. Highly recommended.

---

## Streamlit Cloud Integration

### Two-App Setup (Production + Staging)

| App | Branch | URL | Purpose |
|-----|--------|-----|---------|
| Production | `main` | `ai-compliance-gap-analyzer.streamlit.app` | What users see |
| Staging | `dev` | `ai-compliance-gap-analyzer-staging.streamlit.app` | Test before merging |

- Every PR merge to `main` triggers an automatic redeployment of production
- Every push to `dev` triggers an automatic redeployment of staging
- You can freely experiment on `dev` without risk to users

### Setting Up the Staging App (One-Time)

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click **New app**
3. Select the same repository: `yeyfreya/ai-compliance-gap-analyzer`
4. **Change the branch** from `main` to `dev`
5. Main file path: `streamlit_app.py` (same as production)
6. Click **Advanced settings** → add the same secrets as production:
   ```toml
   ANTHROPIC_API_KEY = "..."
   TAVILY_API_KEY = "..."
   SUPABASE_URL = "..."
   SUPABASE_KEY = "..."
   LANGFUSE_SECRET_KEY = "..."
   LANGFUSE_PUBLIC_KEY = "..."
   LANGFUSE_HOST = "..."
   ```
7. Click **Deploy**

The staging app gets its own URL. Bookmark it for easy access.

### Testing Workflow

1. Work on `dev` locally, test with `streamlit run streamlit_app.py`
2. Push to `dev` — staging app auto-deploys
3. Verify on the staging URL (catches cloud-specific issues: secrets, dependencies, caching)
4. When staging looks good, create PR from `dev → main`
5. Merge — production auto-deploys

### When Staging Matters Most

Local testing covers most cases. The staging app earns its keep when you're changing:
- **Secrets or environment handling** (`st.secrets` logic)
- **Dependencies** (`requirements.txt` — cloud installs fresh)
- **Streamlit-specific features** (caching, session state, cloud-only behavior)
- **Anything that previously broke on cloud but worked locally**

For pure agent logic changes (prompts, pipeline, analysis), local testing is sufficient.

---

## Cheat Sheet

```
Start of session:     git checkout dev
                      git pull origin dev

During work:          git add .
                      git commit -m "v0.X: description"
                      git push origin dev

Ready to release:     gh pr create --base main --head dev --title "v0.X: Release"
                      (merge on GitHub)
                      git checkout main
                      git pull origin main
                      git tag v0.X
                      git push origin v0.X
                      git checkout dev
                      git merge main
                      git push origin dev

Check branch:         git branch
Check tags:           git tag
```
