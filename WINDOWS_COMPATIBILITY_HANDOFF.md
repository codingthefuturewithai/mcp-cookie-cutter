# Windows Compatibility Fix - Session Handoff Document

## Current Status
Date: 2024-12-24
Branch: `fix/windows-compatibility`
Last Working Commit: fa8eaba (main branch)

## Issues Fixed So Far

### 1. ✅ Post-generation Hook platformdirs Import
- **File**: `hooks/post_gen_project.py`
- **Problem**: `platformdirs` not available in cookiecutter environment on Windows
- **Fix**: Made import optional with manual fallback paths

### 2. ✅ Console Output Symbols
- **File**: `hooks/post_gen_project.py`
- **Problem**: Emoji symbols cause copy/paste issues in Windows terminals
- **Fix**: Replaced with bracketed numbers [1], [2], etc.

### 3. ✅ Windows Signal Handling
- **File**: `{{cookiecutter.__project_slug}}/tests/integration/conftest.py`
- **Problem**: `signal.SIGKILL` doesn't exist on Windows
- **Fix**: Added Windows-specific process termination using ctypes

### 4. ✅ Hardcoded Unix Log Paths
- **File**: `{{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/logging_config.py`
- **Problem**: `/var/log/mcp-servers` doesn't exist on Windows
- **Fix**: Added proper Windows paths using environment variables

### 5. ✅ Admin Detection
- **File**: `{{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/logging_config.py`
- **Problem**: `os.geteuid()` is Unix-only
- **Fix**: Added Windows admin detection using ctypes

### 6. ✅ SQLite WAL Mode
- **Files**: 
  - `{{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/log_system/destinations/sqlite.py`
  - `{{cookiecutter.__project_slug}}/{{cookiecutter.__project_slug}}/decorators/sqlite_logger.py`
- **Problem**: WAL mode causes file locking on Windows
- **Fix**: Added try/except to fall back to DELETE mode

### 7. ✅ Claude Commands Windows Compatibility
- **Files**: All `.claude/commands/*.md` files
- **Problem**: Unix-only commands (ps, kill, grep, etc.)
- **Fix**: Added Windows alternatives for all shell commands
- **New File**: Created `_platform_helpers.md` with platform-specific references

## Issues Still To Analyze/Fix

### Critical Priority (Most likely to affect users)

1. **Virtual Environment Activation**
   - Need to check ALL references to venv activation
   - Files to check: README, docs, UI code, tests
   
2. **Process Management Commands**
   - Beyond Claude commands, check if any Python code uses ps/kill
   
3. **Path Separators**
   - Audit ALL Python code for hardcoded forward slashes
   - Check string concatenation vs Path objects
   
4. **Line Endings**
   - Need .gitattributes file for CRLF handling
   - Check if any files have hardcoded \n
   
5. **Shell Commands in Documentation**
   - README.md
   - Any .md files in docs/
   - UI documentation pages
   
6. **File Locking Issues**
   - Check if we try to delete/rename open files anywhere
   - Especially in test cleanup code
   
7. **Long Path Issues**
   - Check if cookiecutter project name could create long paths
   - Windows MAX_PATH = 260 chars
   
8. **Unicode/Emoji**
   - Already fixed in post-gen hook
   - Need to check: UI, logs, test output

## Files That Need Full Audit

### Python Code Files
```
# Core server files
{{cookiecutter.__project_slug}}/server/app.py
{{cookiecutter.__project_slug}}/client/app.py
{{cookiecutter.__project_slug}}/config.py

# All tools
{{cookiecutter.__project_slug}}/tools/*.py

# UI files
{{cookiecutter.__project_slug}}/ui/*.py
{{cookiecutter.__project_slug}}/ui/pages/*.py

# Test files
{{cookiecutter.__project_slug}}/tests/unit/*.py
{{cookiecutter.__project_slug}}/tests/integration/*.py

# Utility files
{{cookiecutter.__project_slug}}/utils/*.py
```

### Documentation Files
```
README.md
{{cookiecutter.__project_slug}}/docs/*.md
{{cookiecutter.__project_slug}}/.reference/*.md
```

### Configuration Files
```
.gitattributes (CREATE if missing)
pyproject.toml
setup.py (if exists)
```

## Test Plan for Windows VM

1. **Fresh Generation Test**
   ```powershell
   cookiecutter gh:codingthefuturewithai/mcp-cookie-cutter --checkout fix/windows-compatibility
   ```

2. **Virtual Environment Test**
   - Test activation commands
   - Test uv commands

3. **Server Start Test**
   - Test stdio mode
   - Test SSE mode
   - Test client connection

4. **UI Test**
   - Start Streamlit
   - Check all pages load
   - Check logs display

5. **Process Management Test**
   - Start server
   - Find process
   - Kill process

6. **Test Suite**
   ```powershell
   uv run pytest
   ```

7. **Long Path Test**
   - Create project with long name
   - Deep directory nesting

## Known Windows-Specific Issues to Watch For

1. **PowerShell Execution Policy**
   - May need: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

2. **Python Launcher**
   - Windows uses `py` command
   - May need `py -m pip` instead of `pip`

3. **Git Line Endings**
   - May need: `git config core.autocrlf true`

4. **Antivirus False Positives**
   - MCP server might trigger Windows Defender
   - Exclude project directory if needed

## Critical Code Patterns to Search For

```python
# BAD - Hardcoded forward slashes
path = "logs/file.txt"
config_path = f"{base_dir}/config.yaml"

# GOOD - Using Path objects
path = Path("logs") / "file.txt"
config_path = base_dir / "config.yaml"

# BAD - Unix commands
os.system("kill -9 " + pid)
subprocess.run(["ps", "aux"])

# GOOD - Cross-platform
process.terminate()
psutil.Process(pid).terminate()

# BAD - Unix-only modules
import pwd
import grp
import fcntl

# BAD - Hardcoded line endings
content = "line1\nline2\n"

# GOOD - Platform-aware
content = f"line1{os.linesep}line2{os.linesep}"
```

## Next Steps for Windows Session

1. Pull the branch on Windows VM
2. Run through the test plan
3. Use this document to continue the audit
4. Search for the code patterns listed above
5. Test each fixed issue to confirm it works
6. Document any new issues found
7. Fix remaining issues
8. Test complete generation-to-deployment flow

## Command to Resume on Windows

```powershell
git clone https://github.com/codingthefuturewithai/mcp-cookie-cutter.git
cd mcp-cookie-cutter
git checkout fix/windows-compatibility
# Open in Claude Code and reference this document
```

Remember: The goal is 100% Windows compatibility. Even one broken command will frustrate users.