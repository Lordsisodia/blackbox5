# Claude Code Hooks Patterns Catalog

**Source:** claude-code-hooks-mastery (92/100 BB5 relevance)
**Analysis Date:** 2026-02-04
**Status:** Complete

---

## Table of Contents

1. [Core Patterns](#core-patterns)
2. [Security Patterns](#security-patterns)
3. [Logging Patterns](#logging-patterns)
4. [TTS Patterns](#tts-patterns)
5. [LLM Integration Patterns](#llm-integration-patterns)
6. [Exit Code Semantics](#exit-code-semantics)
7. [File Organization](#file-organization)
8. [Integration Points](#integration-points)

---

## Core Patterns

### 1. UV Single-File Script Pattern

All hooks use PEP 723 inline dependency declaration:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "anthropic",  # when needed
# ]
# ///
```

**Benefits:**
- No virtualenv management
- Self-contained scripts
- Automatic dependency resolution
- Fast execution

**BB5 Adaptation:** Use for all new hooks, migrate existing bash hooks gradually.

---

### 2. JSON Input/Output Pattern

**Input:** All hooks read JSON from stdin:
```python
input_data = json.loads(sys.stdin.read())
session_id = input_data.get('session_id', 'unknown')
```

**Output (for additionalContext):**
```python
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context_string
    }
}
print(json.dumps(output))
```

**Key Points:**
- `additionalContext` is injected into Claude's prompt (user doesn't see it)
- Only SessionStart and UserPromptSubmit can return additionalContext
- Other hooks should exit silently (0 for success, 2 for block)

---

### 3. Graceful Error Handling Pattern

```python
try:
    # Main logic
    pass
except json.JSONDecodeError:
    sys.exit(0)  # Gracefully ignore JSON errors
except Exception:
    sys.exit(0)  # Never block on hook errors
```

**Principle:** Hooks should never break the user experience. Fail silently.

---

## Security Patterns

### Pre-Tool-Use Security Hook

**Location:** `pre_tool_use.py`

**Capabilities:**
1. **Dangerous rm -rf Blocking**
   ```python
   patterns = [
       r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf variations
       r'\brm\s+--recursive\s+--force',
       r'\brm\s+-r\s+.*-f',
   ]
   dangerous_paths = [r'/', r'/\*', r'~', r'\$HOME', r'\.\.', r'\*', r'\.']
   ```

2. **.env File Access Blocking**
   ```python
   if '.env' in file_path and not file_path.endswith('.env.sample'):
       return True
   ```

**Exit Code:** 2 (blocks tool and shows error to Claude)

**BB5 Consideration:** User wants to allow .env access for agents - customize or skip this rule.

---

## Logging Patterns

### Standard JSON Logging

All hooks use identical logging pattern:

```python
def log_event(input_data, log_filename):
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / log_filename

    # Read existing or init empty
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []

    # Append and write
    log_data.append(input_data)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
```

**Log Files Created:**
- `logs/session_start.json`
- `logs/user_prompt_submit.json`
- `logs/pre_tool_use.json`
- `logs/post_tool_use.json`
- `logs/subagent_start.json`
- `logs/subagent_stop.json`
- `logs/stop.json`

**BB5 Adaptation:** Standardize all RALF hooks to use this pattern.

---

## TTS Patterns

### Priority Chain Pattern

```python
def get_tts_script_path():
    """Priority: ElevenLabs > OpenAI > pyttsx3"""
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"

    if os.getenv('ELEVENLABS_API_KEY'):
        return tts_dir / "elevenlabs_tts.py"
    if os.getenv('OPENAI_API_KEY'):
        return tts_dir / "openai_tts.py"
    return tts_dir / "pyttsx3_tts.py"  # Local fallback
```

### File-Based Locking for Concurrent TTS

**Location:** `utils/tts/tts_queue.py`

Uses `fcntl.flock` for cross-process synchronization:

```python
def acquire_tts_lock(agent_id: str, timeout: int = 30) -> bool:
    fd = os.open(str(_LOCK_FILE), os.O_RDWR | os.O_CREAT, 0o644)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    # Lock acquired
```

**Features:**
- Exponential backoff retry
- Stale lock cleanup (PID checking)
- Lock metadata (agent_id, timestamp, PID)

**BB5 Relevance:** Critical for multi-agent RALF system where multiple agents may trigger TTS simultaneously.

---

## LLM Integration Patterns

### Priority Chain Pattern

```python
def get_llm_completion_message():
    """Priority: OpenAI > Anthropic > Ollama > fallback"""
    if os.getenv('OPENAI_API_KEY'):
        # Try OpenAI
    if os.getenv('ANTHROPIC_API_KEY'):
        # Try Anthropic
    # Try Ollama (local, no API key)
    return random.choice(fallback_messages)
```

### Task Summarization

**Location:** `utils/llm/task_summarizer.py`

Uses Claude Haiku for fast, cost-effective summarization:

```python
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    temperature=0.7,
    messages=[{"role": "user", "content": prompt}],
)
```

**Use Case:** Generate personalized TTS announcements for subagent completion.

---

## Exit Code Semantics

| Code | Meaning | Use Case |
|------|---------|----------|
| 0 | Success / Continue | Normal operation, allow action |
| 2 | Block with error | Security violations, show error to Claude |

**Important:** Exit code 2 only works with:
- `PreToolUse` hook (blocks tool execution)
- `UserPromptSubmit` hook (blocks prompt)

Other hooks cannot block - they only observe/log.

---

## File Organization

```
.claude/
├── hooks/
│   ├── session_start.py
│   ├── session_end.py
│   ├── user_prompt_submit.py
│   ├── pre_tool_use.py
│   ├── post_tool_use.py
│   ├── post_tool_use_failure.py
│   ├── permission_request.py
│   ├── pre_compact.py
│   ├── subagent_start.py
│   ├── subagent_stop.py
│   ├── stop.py
│   ├── notification.py
│   ├── setup.py
│   └── utils/
│       ├── tts/
│       │   ├── elevenlabs_tts.py
│       │   ├── openai_tts.py
│       │   ├── pyttsx3_tts.py
│       │   └── tts_queue.py
│       └── llm/
│           ├── anth.py
│           ├── oai.py
│           ├── ollama.py
│           └── task_summarizer.py
├── data/
│   └── sessions/
│       └── {session_id}.json
└── settings.json
```

---

## Integration Points

### SessionStart Hook Integration

**Current RALF:** Basic session initialization
**Mastery Features to Add:**
1. Git status loading (branch, uncommitted changes)
2. Context file loading (.claude/CONTEXT.md, TODO.md)
3. GitHub issues integration (gh CLI)
4. TTS announcement on session start
5. `additionalContext` injection

### Subagent Tracking Integration

**Current RALF:** No subagent lifecycle hooks
**Mastery Features to Add:**
1. `subagent_start.py` - Log agent spawn with agent_type
2. `subagent_stop.py` - Log completion with task summarization
3. TTS queue management for concurrent agents
4. Transcript export to chat.json

### Security Hook Integration

**Current RALF:** No security hooks
**Mastery Features to Add:**
1. `pre_tool_use.py` with rm -rf blocking
2. Pattern-based command validation
3. JSON logging of all tool calls

---

## Implementation Priority for BB5

### Critical (Week 1)
1. **Pre-Tool-Use Security Hook** - Block dangerous commands
2. **JSON Logging Standardization** - All hooks use same pattern

### High (Week 2)
3. **SessionStart Enhancement** - Git status, context loading
4. **Subagent Tracking** - Lifecycle hooks for Executor/Planner/Architect

### Medium (Week 3-4)
5. **TTS Integration** - Priority chain with queue management
6. **Task Summarization** - LLM-powered completion messages

---

## Files Referenced

- All hooks: `claude-code-hooks-mastery/.claude/hooks/`
- Utilities: `claude-code-hooks-mastery/.claude/hooks/utils/`
- BB5 Tasks: `5-project-memory/blackbox5/.autonomous/tasks/hooks-integration/`
