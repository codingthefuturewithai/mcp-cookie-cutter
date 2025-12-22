---
description: Security analysis - branch changes, full repo, or specific files
argument-hint: "[ISSUE-KEY]"
allowed-tools: ["Task", "Read", "Bash", "Grep", "Glob", "AskUserQuestion"]
---

# Security Review

I'll perform a comprehensive security analysis.

---

## Step 1: Determine Scope

## Note for AI Assistants - DETERMINE SCOPE

Check if $ARGUMENTS is provided:

**If $ARGUMENTS is provided (e.g., "PROJ-123"):**
- Treat as ISSUE-KEY
- Scope: Branch changes for that issue
- Proceed to "Branch Changes Mode" below

**If $ARGUMENTS is empty:**
- Interactive mode
- Ask user what to scan
- Proceed to "Interactive Mode" below

---

### Branch Changes Mode (when ISSUE-KEY provided)

Analyzing branch changes for: $ARGUMENTS

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
  - If ISSUE-KEY: "Analyzing security of changes for $ARGUMENTS"
  - If no ISSUE-KEY: "Security scan of [scope description]"
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

**Scope:** [Branch changes for $ARGUMENTS / Full repository / Specific files / Directory]
**Files Analyzed:** [N] files
**Findings:**
- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- LOW: [count]

[Display detailed findings from agent report]

---

## ✅ Next Steps

**If this was for a specific issue ($ARGUMENTS):**

- **No issues found:**
  ```bash
  /devflow:complete $ARGUMENTS
  ```

- **Vulnerabilities found:**
  1. Review the findings above
  2. Implement the recommended fixes
  3. Re-run this security review:
     ```bash
     /devflow:security-review $ARGUMENTS
     ```
  4. Once clean, proceed to complete:
     ```bash
     /devflow:complete $ARGUMENTS
     ```

**If this was a general security scan:**

- **Vulnerabilities found:** Address the findings above and re-run the scan
- **No issues found:** Your code looks secure!

---

## 🛑 Security Review Complete

The security analysis is finished. Address any findings before proceeding.
