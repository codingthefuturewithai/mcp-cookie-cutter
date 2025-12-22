---
description: Sync with remote after PR merge and clean up
argument-hint: ""
allowed-tools: ["Bash", "Read"]
---

# Post-Merge Sync and Cleanup

I'll sync your local repository with the merged changes and prepare for the next issue.

---

## Step 1: Check Current State

Verify current branch and status:

```bash
git status
git branch --show-current
```

## Note for AI Assistants - CHECK STATE

Use Bash tool to run:
```bash
git status
```

And:
```bash
git branch --show-current
```

Report the current branch and any uncommitted changes.

---

## Step 2: Switch to Main Branch

Return to main branch:

```bash
git checkout main
```

## Note for AI Assistants - SWITCH BRANCH

Use Bash tool to run:
```bash
git checkout main
```

If this fails (e.g., main doesn't exist, try master):
```bash
git checkout master
```

---

## Step 3: Pull Latest Changes

Get the merged PR and any other updates:

```bash
git pull origin main
```

## Note for AI Assistants - PULL CHANGES

Determine base branch (main or master) from Step 2, then use Bash tool to run:
```bash
git pull origin [main|master]
```

Report number of commits pulled and files changed.

---

## Step 4: Verify Merge

Confirm changes are in the base branch:

```bash
git log --oneline -10
```

## Note for AI Assistants - VERIFY MERGE

Use Bash tool to run:
```bash
git log --oneline -10
```

Show recent commits to user.

---

## Step 5: Clean Up Feature Branch

Remove the local feature branch:

```bash
git branch -d [feature-branch-name]
```

## Note for AI Assistants - DELETE BRANCH

1. Get the previous branch name:
```bash
git rev-parse --abbrev-ref @{-1}
```

2. Delete the local branch:
```bash
git branch -d [branch-name-from-step-1]
```

3. Check if remote branch still exists:
```bash
git ls-remote --heads origin [branch-name]
```

4. If remote branch exists and wasn't auto-deleted, ask user:
   "Remote branch [branch-name] still exists. Delete it? (yes/no)"

   If yes:
   ```bash
   git push origin --delete [branch-name]
   ```

---

## Step 6: Update Dependencies (Optional)

Check if dependencies should be updated:

## Note for AI Assistants - UPDATE DEPENDENCIES

Look for dependency files:
- Python: requirements.txt, setup.py, pyproject.toml
- Node.js: package.json, package-lock.json
- Other: Gemfile, go.mod, etc.

If found, ask user: "Would you like to update dependencies? (yes/no)"

If yes:
- **Python**:
  ```bash
  pip install -r requirements.txt
  ```
  Or if using uv:
  ```bash
  uv sync
  ```

- **Node.js**:
  ```bash
  npm install
  ```

- **Other**: Use appropriate package manager

---

## Step 7: Run Tests (Optional)

Verify everything still works after merge:

## Note for AI Assistants - RUN TESTS

Ask user: "Would you like to run tests to verify the merge? (yes/no)"

If yes:
1. Detect test framework from project files
2. Run appropriate test command
3. Report results

---

## ✅ Post-Merge Complete

Your repository is synced and cleaned up.

**Summary:**
- ✅ Switched to main branch
- ✅ Pulled latest changes
- ✅ Deleted feature branch
- [If done] ✅ Updated dependencies
- [If done] ✅ Tests passing

---

## 🚀 Ready for Next Issue

Your environment is ready. When you're ready to start your next issue, run:

```bash
/devflow:fetch-issue [NEW-ISSUE-KEY]
```

This will begin a new development cycle with:
- Fresh JIRA issue fetch and feasibility analysis
- New branch creation (in plan-work → implement)
- Clean workspace

---

## ⛔ STOP HERE

**DO NOT CONTINUE** - The user must explicitly start a new issue when ready.

💡 **Tip**: Keep your main branch updated regularly to avoid merge conflicts!
