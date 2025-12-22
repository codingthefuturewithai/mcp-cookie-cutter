---
description: Security analysis - branch changes, full repo, or specific files
argument-hint: "[--show-dismissed] [ISSUE-KEY]"
allowed-tools: ["Task", "Read", "Bash", "Grep", "Glob", "AskUserQuestion", "Write", "Edit", "mcp__atlassian__getAccessibleAtlassianResources", "mcp__atlassian__createJiraIssue", "mcp__atlassian__getJiraProjectIssueTypesMetadata"]
---

# Security Review

I'll perform a comprehensive security analysis.

---

## Step 0: Parse Arguments

## Note for AI Assistants - PARSE ARGUMENTS

Parse $ARGUMENTS to extract flags and issue key:

```bash
# Check for --show-dismissed flag
if [[ "$ARGUMENTS" == *"--show-dismissed"* ]]; then
    SHOW_DISMISSED=true
    ISSUE_KEY="${ARGUMENTS//--show-dismissed/}"
    ISSUE_KEY="${ISSUE_KEY// /}"  # Remove extra spaces
else
    SHOW_DISMISSED=false
    ISSUE_KEY="$ARGUMENTS"
fi
```

Store these values:
- SHOW_DISMISSED: true/false
- ISSUE_KEY: the actual issue key (or empty if no issue specified)

---

## Step 1: Determine Scope

## Note for AI Assistants - DETERMINE SCOPE

Check if ISSUE_KEY is provided:

**If ISSUE_KEY is provided (e.g., "PROJ-123"):**
- Scope: Branch changes for that issue
- Proceed to "Branch Changes Mode" below

**If ISSUE_KEY is empty:**
- Interactive mode
- Ask user what to scan
- Proceed to "Interactive Mode" below

---

### Branch Changes Mode (when ISSUE-KEY provided)

Analyzing branch changes for: [ISSUE_KEY]

[If SHOW_DISMISSED is true]:
**Note:** --show-dismissed flag detected. Will include previously dismissed issues in the report.

## Note for AI Assistants - BRANCH CHANGES

Use Bash to find modified files since branching from main:

```bash
# Get the base branch (usually main or master)
git rev-parse --verify main >/dev/null 2>&1 && BASE_BRANCH="main" || BASE_BRANCH="master"

# Get all modified files on current branch
git diff --name-only $BASE_BRANCH...HEAD
```

Display list of modified files and proceed to Step 2.

---

### Interactive Mode (when no ISSUE-KEY)

**What would you like to scan?**

## Note for AI Assistants - INTERACTIVE MODE

Use AskUserQuestion tool to ask:

Question: "What scope should I analyze for security vulnerabilities?"
Options:
1. "Full repository" - Scan entire codebase
2. "Current branch changes" - Only files changed on this branch
3. "Specific files" - You specify file paths
4. "Specific directory" - You specify directory path

Based on user's choice:

**Option 1 (Full repository):**
- Use Glob to find all code files (*.py, *.js, *.ts, *.java, etc.)
- Exclude: node_modules/, .venv/, build/, dist/, __pycache__/
- May be large - warn user and confirm
- Proceed to Step 2

**Option 2 (Current branch changes):**
- Same as Branch Changes Mode above
- Proceed to Step 2

**Option 3 (Specific files):**
- Ask user: "Please provide file paths (space-separated)"
- Validate files exist
- Proceed to Step 2

**Option 4 (Specific directory):**
- Ask user: "Please provide directory path"
- Use Glob to find code files in that directory (recursive)
- Proceed to Step 2

---

**Scope determined:**
- [Branch changes / Full repo / Specific files / Specific directory]
- **Files to analyze:** [N] files
- [List files if < 20, otherwise show count and first 10]

---

## Step 2: Invoke Security Scanner Agent

Now I'll analyze these files for security vulnerabilities.

## Note for AI Assistants - INVOKE AGENT

Use the Task tool with subagent_type="security-scanner" to analyze.

Provide the agent with:
- Context:
  - If ISSUE_KEY is set: "Analyzing security of changes for [ISSUE_KEY]"
  - If ISSUE_KEY is empty: "Security scan of [scope description]"
- List of files to focus on
- Request comprehensive analysis following OWASP Top 10 and agent's methodology

The agent will autonomously:
- Read the specified files
- Analyze for vulnerabilities
- Identify unsafe patterns
- Provide remediation guidance

[Launch security-scanner agent via Task tool]

---

## Step 3: Review Agent Findings

[Agent returns security assessment report]

The security scanner has completed its analysis.

---

## 📋 Security Assessment Summary

**Scope:** [Branch changes for [ISSUE_KEY] / Full repository / Specific files / Directory]
**Files Analyzed:** [N] files
**Findings:**
- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- LOW: [count]

[Display detailed findings from agent report]

---

## Step 4: Triage Security Findings (If Issues Found)

## Note for AI Assistants - TRIAGE WORKFLOW

**Only proceed with triage if there are findings. If no issues found, skip to Next Steps section.**

**Before starting triage:**

1. Check SHOW_DISMISSED value (from Step 0)
2. Load previously dismissed issues if they exist:
   ```bash
   if [ -f ".devflow/security/[ISSUE_KEY]-dismissed.json" ]; then
       # Load dismissed issues JSON
       # Parse into array
   fi
   ```

3. **If SHOW_DISMISSED is true:**
   - Display all dismissed issues with their reasons
   - Show: file, line, issue type, severity, reason, dismissed date
   - Then continue to show current findings

4. **If SHOW_DISMISSED is false (default):**
   - Filter out dismissed issues from current scanner findings
   - Only show new/unaddressed findings in triage loop

5. If issues were found by security scanner (after filtering), proceed with triage

**For each finding from security scanner:**

---

### Finding [X] of [TOTAL]: [Vulnerability Type] ([SEVERITY] severity)

**File:** [file_path]:[line_number]

**Current code:**
```
[show code snippet]
```

**Issue:** [Description of vulnerability]

**Recommended fix:**
```
[show recommended fix]
```

---

**What would you like to do with this finding?**

Type one of the following:
1. **"fix"** - Apply the recommended fix now
2. **"dismiss [reason]"** - Mark as false positive, accepted risk, or not applicable
   - Examples: "dismiss false positive", "dismiss test code only", "dismiss accepted risk"
3. **"ticket"** - Create JIRA issue to track this for later
4. **"manual"** - I'll fix this myself, skip for now
5. **"skip"** - Defer decision to next security review

## Note for AI Assistants - HANDLE RESPONSE

[WAIT FOR USER RESPONSE BEFORE CONTINUING]

**After user responds:**

**If "fix":**
- Use Edit tool to apply the recommended fix to the file
- Track as "applied" in fixes list
- Continue to next finding

**If "dismiss [reason]":**
- Extract reason from user response (everything after "dismiss ")
- If no reason provided, reason = "dismissed"
- Create `.devflow/security/` directory if doesn't exist:
  ```bash
  mkdir -p .devflow/security
  ```
- Load existing dismissed.json or create empty array
- Append to dismissed issues:
  ```json
  {
    "file": "[file_path]",
    "line": [line_number],
    "issue_type": "[vulnerability type]",
    "severity": "[severity]",
    "reason": "[reason from user]",
    "dismissed_at": "[current ISO timestamp]",
    "code_snippet": "[current code]"
  }
  ```
- Write back to `.devflow/security/[ISSUE_KEY]-dismissed.json`
- Track as "dismissed" in summary
- Continue to next finding

**If "ticket":**
- Get cloud ID: `mcp__atlassian__getAccessibleAtlassianResources`
- Extract project key from ISSUE_KEY (part before hyphen)
- Get project metadata: `mcp__atlassian__getJiraProjectIssueTypesMetadata` for the project
- Map severity to priority:
  - CRITICAL → Highest
  - HIGH → High
  - MEDIUM → Medium
  - LOW → Low
- Create JIRA issue with `mcp__atlassian__createJiraIssue`:
  ```json
  {
    "cloudId": "[cloudId]",
    "projectKey": "[project_key]",
    "issueTypeName": "Bug",
    "summary": "[Security] [Vulnerability Type] in [filename]",
    "description": "**Security Finding from [ISSUE_KEY]**\n\n**File:** [file]:[line]\n\n**Vulnerability:** [type] ([severity] severity)\n\n**Issue:**\n[description]\n\n**Current Code:**\n```\n[code]\n```\n\n**Recommended Fix:**\n```\n[fix]\n```\n\n**Security Review Date:** [timestamp]\n**Original Issue:** [ISSUE_KEY]",
    "additional_fields": {
      "priority": { "name": "[mapped priority]" }
    }
  }
  ```
- Display ticket key to user
- Track as "ticketed" in summary with ticket key
- Continue to next finding

**If "manual":**
- Track as "manual" in summary
- Continue to next finding
- (Will appear in next security-review run)

**If "skip":**
- Track as "deferred" in summary
- Continue to next finding
- (Will appear in next security-review run)

**Repeat for all findings.**

---

## Triage Summary

After all findings have been triaged:

📋 **Triage Complete**

**Applied fixes:** [count]
[If count > 0, list each:]
- [file]:[line] - [vulnerability type]

**Dismissed:** [count]
[If count > 0, list each:]
- [file]:[line] - [reason]

**Created tickets:** [count]
[If count > 0, list each:]
- [TICKET-KEY]: [vulnerability type] in [file]

**Manual/Deferred:** [count]
[If count > 0, note that these will show up in next review]

---

[If any fixes were applied]:

**Committing security fixes...**

```bash
git add [list of fixed files]
git commit -m "fix: Address [count] security vulnerabilities from [ISSUE_KEY]

[For each fix:]
- Fix [vulnerability type] in [file]:[line]

Security review: [applied count] fixed, [dismissed count] dismissed, [ticketed count] ticketed

Refs: [ISSUE_KEY]"
```

✅ **Commit:** [commit hash]

---

[If any dismissals]:

📝 **Dismissed issues documented in:** `.devflow/security/[ISSUE_KEY]-dismissed.json`

Future security-review runs will skip these issues automatically.

To review dismissed issues: `/devflow:security-review --show-dismissed [ISSUE_KEY]`

---

## ✅ Next Steps

**If this was for a specific issue (ISSUE_KEY is set):**

- **No issues found OR all issues triaged:**

  [Check if any CRITICAL or HIGH severity issues remain unaddressed]

  [If critical/high issues remain (marked as manual/deferred/skipped)]:
  ⚠️ **Warning:** You have unaddressed CRITICAL or HIGH severity issues. Consider:
  - Re-running triage to fix or ticket them
  - Or explicitly accepting the risk before proceeding

  [If no critical/high issues OR all handled]:
  ✅ **Ready to proceed:**
  ```bash
  /devflow:complete [ISSUE_KEY]
  ```

- **Want to re-run security review:**

  If you manually fixed issues or want to verify fixes:
  ```bash
  /devflow:security-review [ISSUE_KEY]
  ```

**If this was a general security scan:**

- **Issues found:** Triage complete - review summary above
- **No issues found:** Your code looks secure!
- **Re-scan after manual fixes:** `/devflow:security-review [ISSUE-KEY]`

---

## 🛑 Security Review Complete

Security analysis and triage finished. Review the triage summary above before proceeding.
