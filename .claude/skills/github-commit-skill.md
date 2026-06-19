# Github-Commit-Skill — stock-analysis-viewer

## Purpose
Commit MacBook manual changes to `github.com/FinixLLC/stock-analysis-viewer` without conflicting with the daily Lenovo pipeline commits.

## Repo
- Local: `/Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages`
- Remote: `git@github.com:FinixLLC/stock-analysis-viewer.git`
- Pipeline (Lenovo) pushes to `main` every weekday with data files

## The Rule: Always pull before committing

```bash
REPO=/Volumes/1T_ExFAT/StockScan/devcpp/Sarah2/src/stock-analysis-pages

# 1. Pull remote changes first (rebase local work on top)
git -C $REPO pull --rebase origin main

# 2. Stage only the files YOU changed (never use git add -A)
git -C $REPO add <your specific files>

# 3. Commit
git -C $REPO commit -m "your message"

# 4. Push
git -C $REPO push origin main
```

## If push is rejected (remote has new pipeline commits)

```bash
git -C $REPO pull --rebase origin main
git -C $REPO push origin main
```

## If "cannot pull with rebase: You have unstaged changes"

The working tree has pipeline-generated files that differ from HEAD (file permissions, new data). These are NOT your changes — ignore them:

```bash
# Discard working-tree-only pipeline file changes, then pull
git -C $REPO config core.fileMode false   # suppress permission-only diffs
git -C $REPO restore .                    # reset tracked-file changes to HEAD
git -C $REPO pull --rebase origin main
git -C $REPO push origin main
```

## Files owned by the pipeline — never commit these manually
- `patterns/*.txt`
- `top50/*.csv`
- `top_20_momentum_*.txt`
- `top-picks.json`
- `portfolio-summary.json`
- `file-list.json`
- `enhanced-trends/*.json`
- `company-profiles/*.json`
- `financial_reports/*.txt`
- `deepseek-reports/`

## Files safe to commit manually
- `index.html`, `enhanced-trends.html`, `company-profile.html`, `portfolio.html`
- `favicon.svg`
- `INTRODUCTION.md`
- Any new `.html`, `.css`, `.js` viewer files
