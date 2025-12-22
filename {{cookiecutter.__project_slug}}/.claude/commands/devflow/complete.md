---
description: Final validation, create PR, and mark JIRA done
argument-hint: "[ISSUE-KEY]"
allowed-tools: ["Bash", "mcp__atlassian__getJiraIssue", "mcp__atlassian__getAccessibleAtlassianResources", "mcp__atlassian__transitionJiraIssue", "mcp__atlassian__getTransitionsForJiraIssue", "Read", "Grep", "Glob"]
---

# Complete Work

I'll run final validation, create a PR, and update JIRA to Done.

Issue: $ARGUMENTS

---

## 🔒 Recommended Prerequisites

**Security review recommended before running complete:**

If you haven't already, consider running:
```bash
/devflow:security-review $ARGUMENTS
```

This is especially important if your changes involve authentication, input validation, database queries, or other security-sensitive code.

**Skip if:**
- You already ran security-review and addressed all findings
- Changes are documentation-only or other low-risk refactoring
- You want to proceed without security analysis

---

## Step 1: Final Validation

**Strategy adapts to work type:**

**For code with tests:**
- Discover test command from project files (package.json, Makefile, README, etc.)
- Check for coverage tools (pytest-cov, coverage.py, jest --coverage, go test -cover, simplecov)
- Run full test suite (with coverage if available)
- Verify all tests pass
- Report coverage summary if available

**For bug fixes:**
- Run affected test suite
- Verify regression test passes
- Confirm bug no longer reproduces

**For infrastructure/config:**
- Trigger validation (build, workflow, deployment dry-run)
- Verify expected behavior
- Check logs/output

**For documentation:**
- Verify accuracy of changes
- Test any code examples
- Check links work

[Run appropriate validation]

**Validation Results:**

[If tests exist]:
- **Tests:** [X] passed, [Y] failed
- **Coverage** (if available): [Z]% overall
  - New/modified files: [list with coverage %]
  - Coverage change: [+/-X]% vs previous

[Otherwise]:
[Report results - builds, checks, etc.]

⚠️ If validation fails, STOP - must fix before proceeding

✅ Validation passed

---

## Step 2: Fetch JIRA Issue

[Call `mcp__atlassian__getAccessibleAtlassianResources`]
[Call `mcp__atlassian__getJiraIssue`]

Issue: [ISSUE-KEY] - [Summary]

---

## Step 3: Analyze Changes for PR

```bash
git diff --name-only [base-branch]...HEAD
git log --oneline [base-branch]...HEAD
```

[Read key changed files to understand implementation]

**Changes Summary:**
- [What was implemented/fixed]
- [Key files modified]
- [How it addresses JIRA requirements]

---

## Step 4: Create Pull Request

Using GitHub CLI to create PR with auto-generated description.

**Title:** [ISSUE-KEY]: [Issue Summary]

**Body:**
```markdown
Fixes [ISSUE-KEY]

## Summary
[What was implemented and how it addresses requirements]

## Changes
- [Key changes with file paths]

## Validation
- [Validation approach used]
- [Results summary]
- [If tests exist: Tests: X passed, Coverage: Y%]

**JIRA:** [link to issue]
```

```bash
gh pr create --title "[ISSUE-KEY]: [Summary]" --body "[generated description]"
```

✅ PR: [URL]

---

## Step 5: Update JIRA

[Call `mcp__atlassian__getTransitionsForJiraIssue`]
[Call `mcp__atlassian__transitionJiraIssue` to "Done"]

✅ JIRA: [ISSUE-KEY] → Done

---

## ✅ Complete

**Summary:**
- ✅ Validation passed
- ✅ PR created: [URL]
- ✅ JIRA: Done

**Next Steps:**
1. Review PR or request reviews
2. Address feedback if any
3. Merge when approved
4. **After PR is merged,** run post-merge cleanup:
   ```bash
   /devflow:post-merge
   ```

The post-merge command will:
- Switch back to main branch
- Pull the merged changes
- Delete the feature branch
- Update dependencies (optional)
- Run tests to verify (optional)

---

Work complete! Remember to run `/devflow:post-merge` after your PR is merged.
