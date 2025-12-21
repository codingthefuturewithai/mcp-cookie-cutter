---
description: Sync with remote after PR merge and clean up
argument-hint: ""
allowed-tools: ["Bash", "Read"]
---

## Post-Merge Sync and Cleanup - FileOrbit Development

I'll sync your local repository with the merged changes and prepare for the next issue.

### Step 1: Check Current State
Verify current branch and status:

!git status
!git branch --show-current

### Step 2: Switch to Main
Return to main branch:

!git checkout main

### Step 3: Pull Latest Changes
Get the merged PR and any other updates:

!git pull origin main

### Step 4: Verify Merge
Confirm your changes are in main:

!git log --oneline -10

### Step 5: Clean Up Feature Branch
Remove the local feature branch:

!git branch -d $(git rev-parse --abbrev-ref @{-1})

Optional: Remove remote branch if not auto-deleted:
!git push origin --delete $(git rev-parse --abbrev-ref @{-1})

### Step 6: Update Dependencies
Ensure environment is current:

# Python dependencies
!pip install -r requirements.txt
# Or if using UV: !uv sync
# Check if Docker images need rebuilding
!docker-compose build --no-cache # if containers were modified

### Step 7: Run Tests
Verify everything still works after merge:

!pytest # Backend tests
# Future: npm test for frontend when configured
# Verify distributed services if needed: docker-compose up -d && pytest integration/

---

## ⛔ STOP HERE - Post-Merge Complete

**I have synced your repository and cleaned up. I will NOT fetch a new issue.**

## 🚀 Ready for Next Issue!

Your environment is clean and ready. When YOU are ready to start your next issue, run:

```
/project:devflow/fetch-issue [NEW-CP-ISSUE] fileorbit
```

This will begin a new development cycle with:
- Fresh JIRA issue fetch
- New feature/CP-XX-description branch
- Clean workspace

**DO NOT CONTINUE** - The user must explicitly start a new issue when ready.

💡 **Tips**: 
- Keep your main branch updated regularly to avoid conflicts!
- Remember FileOrbit's distributed architecture when planning changes
- Check CLAUDE.md for latest project status and component interactions