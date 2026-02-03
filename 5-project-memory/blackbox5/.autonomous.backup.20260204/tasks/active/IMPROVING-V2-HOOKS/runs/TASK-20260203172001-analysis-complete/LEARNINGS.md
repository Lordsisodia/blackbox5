# LEARNINGS: TASK-20260203172001 - Hook Patterns Analysis

## What Worked Well

### Parallel Subagent Analysis
Spawning 4 subagents simultaneously was highly effective. Each agent focused on a specific domain:
- Session patterns
- Security patterns
- Lifecycle patterns
- Utility patterns

Result: Comprehensive coverage in single session.

### UV Single-File Scripts
The PEP 723 inline dependency declaration is a game-changer:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-dotenv"]
# ///
```
No requirements.txt, no virtualenv, just `uv run script.py`.

### File-Based TTS Locking
Using `fcntl.flock` for cross-process TTS coordination is elegant:
- Works across different Python processes
- Automatic cleanup on process exit
- No external dependencies

## Surprising Discoveries

### Exit Code 2 Semantics
Exit code 2 is the ONLY way to block tool execution and show error to Claude. Exit code 1 just fails silently. This is critical for security hooks.

### additionalContext Injection
SessionStart can inject context into Claude's prompt that the user doesn't see. Perfect for loading project context automatically.

### Task Summarization Cost
Using Claude Haiku for task summarization is extremely cost-effective:
- 100 tokens max
- Fast response
- Good enough for TTS announcements

## What Was Harder Than Expected

### Pattern Extraction
Extracting patterns from 13 hooks + utilities took longer than expected. Each hook has subtle variations that needed documentation.

### Integration Mapping
Mapping mastery patterns to BB5 RALF required understanding both systems deeply. Not all patterns translate directly.

## What Would I Do Differently

1. **Start with patterns catalog** - Document patterns as we discover them, not at end
2. **Create comparison matrix** - Side-by-side mastery vs RALF from the start
3. **Tag patterns by priority** - Mark critical/high/medium during analysis, not after

## Patterns for Future Use

### JSON Logging Pattern
```python
log_file = Path("logs/hook_name.json")
log_data = json.load(log_file) if log_file.exists() else []
log_data.append(input_data)
json.dump(log_data, f, indent=2)
```
Use this for ANY event logging in BB5.

### Priority Chain Pattern
```python
if os.getenv('SERVICE_API_KEY'):
    return primary_service()
if os.getenv('FALLBACK_API_KEY'):
    return fallback_service()
return local_fallback()
```
Use for any service with alternatives (TTS, LLM, etc).

### Graceful Degradation
```python
try:
    # Main logic
except Exception:
    sys.exit(0)  # Never block on hook errors
```
All hooks should fail silently.
