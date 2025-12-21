# Bug Issue Example

This example shows the **structure and pattern** for Bug issues, based on ACT-96 and industry best practices.

**🎯 HOW TO USE THIS EXAMPLE:**

This is a real bug from a Python CLI project. Your bug might be in:
- Web app, REST API, mobile app
- Database, infrastructure, DevOps
- Frontend, backend, integration layer

**Adapt the pattern to your domain** - don't copy verbatim. Focus on:
✅ The structure (Problem → Environment → Reproduce → Behavior → Analysis)
✅ Detailed reproduction steps
✅ Identifying problem areas, not dictating exact fixes

⚠️ **CRITICAL**: Read REFERENCE.md § "Bug Report Standards" for guidance on "Investigation Areas" vs "Prescriptive Solutions".

---

## Example: [Windows] OpenAI API Key Not Being Read from Config File

**Problem Statement:**
Users on Windows are unable to use RAG Retriever due to the application failing to read the OpenAI API key from the config file, despite correct configuration.

**Reference:**
Original GitHub Issue: https://github.com/codingthefuturewithai/rag-retriever/issues/6

**Environment:**
* OS: Windows 11
* Shell: Git Bash, PowerShell, and CMD (issue occurs in all shells)
* Installation Method: pipx
* Installation Path: C:\\Users\\User\\.local\\bin\\rag-retriever.exe

**Steps to Reproduce:**

1. Install RAG Retriever using pipx: `pipx install rag-retriever`
2. Run `rag-retriever --init` to create config file
3. Create/verify directory exists: `%APPDATA%\\rag-retriever`
4. Create/edit config.yaml with valid OpenAI API key:
   ```yaml
   api:
     openai_api_key: "sk-your-key-here"
   ```
5. Attempt to use RAG Retriever with any command (e.g., `rag-retriever --ingest-directory`)

**Current Behavior:**
* Error message: "ERROR:rag_retriever.cli:Error ingesting documents: OpenAI API key not found"
* Debug logs show API key is found in config but parsed as None type
* Setting OPENAI_API_KEY environment variable works as temporary workaround

**Expected Behavior:**
* Application should successfully read the API key from config.yaml
* No error message about missing API key when config file is properly set up

**Debug Information:**
```
DEBUG:rag_retriever.utils.config:Config keys available: ['vector_store', 'document_processing', 'content', 'search', 'browser', 'image_processing', 'api']
DEBUG:rag_retriever.utils.config:API section found in config
DEBUG:rag_retriever.utils.config:API section keys: ['openai_api_key', 'confluence']
DEBUG:rag_retriever.utils.config:openai_api_key found in config
DEBUG:rag_retriever.utils.config:API key type: <class 'NoneType'>
DEBUG:rag_retriever.utils.config:API key starts with sk-: False
```

**Workaround:**
Set the API key as an environment variable:
```powershell
set OPENAI_API_KEY=sk-your-key-here
```

**Root Cause Analysis:**
The debug logs indicate the YAML file is being read and the `openai_api_key` field is found, but it's being parsed as NoneType instead of the actual string value. This suggests a YAML parsing issue specific to Windows file encoding or path resolution.

**Investigation Areas:**
Based on debug logs, the problem appears to be in:
1. **Config file parsing logic** - YAML file is read but key value becomes None
2. **File encoding handling** - May need explicit UTF-8 encoding on Windows
3. **Windows path resolution** - %APPDATA% directory handling may differ
4. **Type validation** - No validation that parsed value is actually a string

**Potential Approaches:**
- Add explicit encoding specification when reading YAML files
- Add type validation and clear error messages for config values
- Add Windows-specific test coverage for config loading
- Consider using platform-agnostic config file locations

⚠️ **Note**: These are investigation areas and suggested directions, not prescriptive implementation steps. Developers should diagnose and implement the fix that best fits the codebase architecture.

**Testing Requirements:**
* Verify fix works on Windows 11 with Git Bash, PowerShell, and CMD
* Test with special characters in API key
* Verify no regression on Unix-based systems (macOS, Linux)
* Add unit test for config loading with UTF-8 encoding

**Priority:** Medium

**Labels:** (none in original, but could be: `windows`, `bug`, `config`, `yaml`)

---

## Key Characteristics to Emulate:

1. **Problem Statement**:
   - 1-2 sentence summary of the issue and user impact
   - Clear and concise

2. **Reference** (Optional):
   - Link to external issue tracker, support ticket, or related documentation

3. **Environment**:
   - Very detailed environment information
   - OS, versions, installation method, paths
   - All relevant technical details

4. **Steps to Reproduce**:
   - Numbered steps with specific commands
   - Include exact file contents and configuration
   - Specific enough that anyone can reproduce

5. **Current vs Expected Behavior**:
   - Separate sections for what happens vs what should happen
   - Include error messages in code blocks

6. **Debug Information** (If available):
   - Stack traces, debug logs, diagnostic output
   - Use code blocks for formatting

7. **Workaround** (If available):
   - Temporary solution while fix is developed
   - Include exact commands or steps

8. **Root Cause Analysis** (If known/suspected):
   - Technical explanation of what's causing the issue
   - Based on codebase examination and debug logs

9. **Investigation Areas**:
   - Components/subsystems where the problem likely exists
   - What the logs/evidence point to
   - Areas that need attention

10. **Potential Approaches**:
    - Suggested directions for fixing (not exact code changes)
    - Alternative strategies to consider
    - General guidance, not prescriptive implementation

11. **Testing Requirements**:
    - How to verify the fix
    - Platforms/environments to test
    - Regression tests needed

## What Makes This a Good Bug Report:

✅ **Comprehensive Environment Details**: OS, shell, installation method, paths
✅ **Reproducible Steps**: Exact commands and file contents
✅ **Diagnostic Information**: Debug logs showing the issue
✅ **Workaround Provided**: Temporary solution for users
✅ **Technical Analysis**: Root cause investigation with evidence from logs
✅ **Investigation Guidance**: Identifies problem areas without micromanaging the fix
✅ **Clear Current vs Expected**: Separate sections for clarity
✅ **Suggestive Approaches**: Points developers in the right direction without dictating exact code changes
