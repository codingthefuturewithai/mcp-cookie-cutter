# COMPLETE SAAGA vs Current MCP Cookie Cutter Analysis

## FOUND ALL SAAGA/OAuth REFERENCES (via grep):

### Files with SAAGA references:
1. **server/app.py** - 10 occurrences:
   - Line 1: "MCP Server with SAAGA Decorators"
   - Line 4: "SAAGA decorators"
   - Line 27: "with SAAGA decorators"
   - Line 85: "using SAAGA decorators"
   - Line 95: "Import SAAGA decorators"
   - Line 101: "Register regular tools with SAAGA decorators"
   - Line 103: "Apply SAAGA decorator chain"
   - Line 117: "Register parallel tools with SAAGA decorators"
   - Line 119: "Apply SAAGA decorator chain"
   - Line 133: "initialized with SAAGA decorators"

2. **tools/example_tools.py** - 2 occurrences:
   - Line 4: "with the SAAGA decorator pattern"
   - Line 23: "decorated with SAAGA decorators"

3. **SETUP_PROMPT.md** - 1 occurrence:
   - "No OAuth/Bazel/SAAGA"

4. **.reference/** files - OAuth mentions only (these are reference docs, may be OK):
   - mcp-quick-reference.md
   - mcp-sdk-knowledge-base.md
   - mcp-version-tracker.md

## FILES THAT NEED FIXES:

### 1. server/app.py - 10 SAAGA references to remove
### 2. tools/example_tools.py - 2 SAAGA references to remove  
### 3. tests/integration/conftest.py - Remove errlog=sys.stderr parameter (line 238)
### 4. tests/integration/test_example_tools_integration.py - NEED TO COPY FROM SAAGA
### 5. tests/unit/test_decorators.py - NEED TO COPY FROM SAAGA (current has wrong tests)
### 6. SETUP_PROMPT.md - Has "SAAGA" reference

## OTHER FILES TO CHECK FOR SAAGA/OAuth:
- All decorator files in decorators/
- All log_system files
- pyproject.toml
- README.md
- DEVELOPMENT.md

## CRITICAL FIXES NEEDED:

## 1. server/app.py

### SAAGA References to Remove:
- Line 1: "SAAGA Decorators" in docstring
- Line 4: "SAAGA decorators" in docstring  
- Line 27: "SAAGA decorators" in function docstring
- Line 32: "SAAGA decorators" in another docstring (needs checking)
- Line 85: "SAAGA decorators" in register_tools docstring
- Line 95: Comment "Import SAAGA decorators"
- Line 101: Comment "Apply SAAGA decorator chain"
- Line 117: Comment "Register parallel tools with SAAGA decorators"
- Line 133: f-string "initialized with SAAGA decorators"

### OAuth References to Remove:
- Lines 27-29 in SAAGA template (oauth import) - ALREADY REMOVED
- Lines 108-110 in SAAGA template (oauth decorator import) - ALREADY REMOVED
- Lines 145-165 in SAAGA template (oauth tool registration) - ALREADY REMOVED

### Other Differences:
- Template variables ({{ cookiecutter.__project_slug }}) replaced with mcp_server_project - CORRECT
- Template conditionals removed (since we're in generated project) - CORRECT

## 2. tools/example_tools.py

### Status: ALREADY CORRECT
- No SAAGA references
- No OAuth references
- Exact match to SAAGA template with template vars rendered

## 3. tests/integration/conftest.py

### Critical Error:
- Line 238: Current has `errlog=sys.stderr` parameter that DOESN'T EXIST in SAAGA
- MUST REMOVE this parameter

### SAAGA References:
- Need to check for any SAAGA references in comments

## 4. tests/integration/test_example_tools_integration.py

### Status: NOT COPIED YET
- Need to copy from SAAGA template
- Remove any SAAGA references in docstrings/comments
- No OAuth sections in this file

## 5. tests/unit/test_decorators.py  

### Status: NOT COPIED YET
- Need to copy from SAAGA template
- Current has TestTypeConverter class that DOESN'T EXIST in SAAGA
- Missing TestSQLiteLogger class that EXISTS in SAAGA
- Remove any SAAGA references

## Files to Check:

### Core Files:
- [ ] server/app.py - NEEDS SAAGA REMOVAL
- [x] tools/example_tools.py - CORRECT
- [ ] tools/echo.py - NEED TO CHECK
- [ ] config.py - NEED TO CHECK
- [ ] logging_config.py - NEED TO CHECK

### Decorator Files:
- [ ] decorators/exception_handler.py - NEED TO CHECK
- [ ] decorators/tool_logger.py - NEED TO CHECK  
- [ ] decorators/type_converter.py - NEED TO CHECK
- [ ] decorators/parallelize.py - NEED TO CHECK

### Log System Files:
- [ ] log_system/correlation.py - NEED TO CHECK
- [ ] log_system/unified_logger.py - NEED TO CHECK
- [ ] log_system/destinations/base.py - NEED TO CHECK
- [ ] log_system/destinations/factory.py - NEED TO CHECK
- [ ] log_system/destinations/sqlite.py - NEED TO CHECK

### Test Files:
- [ ] tests/integration/conftest.py - NEEDS FIX (errlog parameter)
- [ ] tests/integration/test_example_tools_integration.py - NEEDS COPY
- [ ] tests/unit/test_decorators.py - NEEDS COPY
- [ ] tests/unit/test_config.py - NEED TO CHECK
- [ ] tests/unit/test_correlation.py - NEED TO CHECK

### Other Files:
- [ ] pyproject.toml - NEED TO CHECK
- [ ] README.md - NEED TO CHECK  
- [ ] DEVELOPMENT.md - NEED TO CHECK
- [ ] SETUP_PROMPT.md - NEED TO CHECK

## IMMEDIATE FIXES REQUIRED:

1. **server/app.py**: Remove ALL "SAAGA" text (9 occurrences)
2. **tests/integration/conftest.py**: Remove `errlog=sys.stderr` parameter
3. **tests/integration/test_example_tools_integration.py**: Copy from SAAGA
4. **tests/unit/test_decorators.py**: Copy from SAAGA

## NEXT STEPS:
Will systematically check EVERY other file for:
- SAAGA/Saga references
- OAuth references  
- Incorrect modifications