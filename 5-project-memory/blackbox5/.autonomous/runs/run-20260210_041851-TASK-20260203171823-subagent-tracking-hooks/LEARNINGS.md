# LEARNINGS - TASK-20260203171823

## 1. Hook Development Pattern

**Finding:** BB5 hooks follow a consistent pattern for JSON input/output.

**Details:**
- Read JSON from stdin using `json.load(sys.stdin)`
- Add fields to input dict (e.g., `logged_at`)
- Write log files in JSON array format
- Exit with 0 on success, handle errors gracefully

**Reference:** `retain-on-complete.py` shows the established pattern.

## 2. JSONL Transcript Structure

**Finding:** Subagent transcripts use JSONL format with user message entries.

**Details:**
- Each line is a JSON object
- User messages have `type: "user"`
- Content is in `message.content` (nested) or direct `content`
- Can contain arrays of content blocks

**Example Entry:**
```json
{
  "type": "user",
  "message": {
    "content": "Analyze the codebase"
  }
}
```

## 3. Flexible Transcript Path Handling

**Finding:** Input may contain either `agent_transcript_path` or `transcript_path`.

**Details:**
- Different RALF configurations use different field names
- Need to check both in order of preference
- Fallback to generic message if neither exists

**Pattern:**
```python
transcript_path = input_data.get("agent_transcript_path")
if not transcript_path:
    transcript_path = input_data.get("transcript_path")
```

## 4. Content Extraction Complexity

**Finding:** Content can be string, dict, or list of dicts.

**Details:**
- Direct `content` field (string or dict)
- Nested `message.content` (dict with "content" key)
- Array of content blocks with `type="text"` keys

**Extraction Pattern:**
```python
# Try nested path first
content = message.get("content", "")
# Then try direct path
if not content:
    content = entry.get("content")
# Then check array of blocks
if isinstance(content, list):
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text", "")
```

## 5. Heuristic Summarization Effectiveness

**Finding:** Simple heuristic works well for initial MVP.

**Details:**
- Takes first sentence (split by ".")
- Falls back to comma-separated (split by ",")
- Truncates to 100 chars if no punctuation

**Trade-off:** Better than nothing, but can be improved with LLM.

## 6. Log Directory Creation

**Finding:** Always create log directory before writing files.

**Details:**
- `os.makedirs(path, exist_ok=True)` is idempotent
- Safe to call even if directory exists
- Don't need to check existence first

**Pattern:**
```python
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)
```

## 7. Executable Permissions

**Finding:** Hooks must be executable for RALF to run them.

**Details:**
- Use `chmod +x` on Python scripts
- Or shebang line: `#!/usr/bin/env python3`
- RALF looks for executable files

## 8. Settings.json Hook Registration

**Finding:** Hook registration is simple key-value in settings.json.

**Details:**
- `enabled: true` enables the hook
- `path` specifies the script file
- Hooks are called in order listed

**Structure:**
```json
{
  "hooks": {
    "hook_name": {
      "enabled": true,
      "path": ".claude/hooks/hook_name.py"
    }
  }
}
```

## 9. Graceful Error Handling

**Finding:** Hooks should never crash the main session.

**Details:**
- Catch `json.JSONDecodeError` separately
- Catch all exceptions and exit 0
- Fail silently but log errors if possible

**Rationale:** Hook failures should not prevent user work from proceeding.

## 10. Reusable Utility Modules

**Finding:** It's beneficial to extract common logic into utilities.

**Details:**
- Task summarization logic used by both hooks
- Can be tested independently
- Easy to extend with LLM later

**Pattern:**
- Create `utils/task_summarizer.py`
- Import with `sys.path.insert(0, ...)`
- Provide clear public API

## 11. Subagent Tracking Use Cases

**Finding:** These hooks enable critical observability for multi-agent systems.

**Use Cases:**
- Debugging agent coordination issues
- Auditing agent decision paths
- Analyzing task handoffs between agents
- Optimizing agent workflow efficiency
- Understanding agent behavior patterns

## 12. Future LLM Integration Point

**Finding:** Heuristic summarization has a clear path to LLM enhancement.

**Integration Points:**
- Add `summarize_with_llm()` function to `task_summarizer.py`
- Use Ollama API for local LLM
- Keep heuristic as fallback for no-LLM cases
- All hook code stays the same

**API Example:**
```python
def summarize_with_llm(task_context, agent_name):
    response = ollama_client.generate(
        model="llama3",
        prompt=f"Summarize this task: {task_context}"
    )
    return f"Agent {agent_name}: {response}"
```
