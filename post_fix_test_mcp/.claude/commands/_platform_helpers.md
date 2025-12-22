---
description: Platform-specific helper commands for Windows/Mac/Linux compatibility
---

# Platform-Specific Command Helpers

## Process Management Commands

### Check for Running Processes
**Windows (PowerShell):**
```powershell
Get-Process | Where-Object {$_.ProcessName -match "python|uv"} | Select-Object Id, ProcessName, CommandLine
```

**Windows (CMD):**
```cmd
tasklist | findstr /I "python uv"
```

**Mac/Linux:**
```bash
ps aux | grep -E "mcp|uv run" | grep -v grep
```

### Kill Processes
**Windows:**
```cmd
taskkill /PID [PID] /F
```

**Mac/Linux:**
```bash
kill [PID]
```

## Virtual Environment Activation

### Detect and Show Correct Command
**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

## Path Handling

### Always use forward slashes in Python code:
```python
from pathlib import Path
# This works on ALL platforms:
tools_dir = Path("tools")
test_file = Path("tests/integration/test_example.py")
```

### For shell commands, use platform detection:
```python
import platform
if platform.system() == "Windows":
    activate_cmd = r".venv\Scripts\activate"
else:
    activate_cmd = "source .venv/bin/activate"
```

## Python Command Execution

### Cross-platform Python commands:
```bash
# Use double quotes for Windows compatibility
python -c "from module import func; print('works')"

# NOT single quotes (breaks on Windows CMD):
# python -c 'from module import func; print("fails")'
```

## Directory Listing

### Cross-platform directory commands:
**All platforms (using Python):**
```bash
python -c "import os; print('\n'.join(os.listdir('tools')))"
```

**PowerShell/Bash compatible:**
```bash
ls tools/
```

**Windows CMD only:**
```cmd
dir tools\
```