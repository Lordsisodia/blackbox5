---
repo: disler/claude-code-hooks-mastery
url: https://github.com/disler/claude-code-hooks-mastery
stars: 2200
forks: 482
analyzed_at: 2026-02-03T23:45:00Z
analyst: Claude

ratings:
  actionability: 35/35
  bb5_relevance: 28/30
  pattern_quality: 19/20
  innovation: 10/15
  total: 92/100

classification:
  type: educational
  areas: [hooks, lifecycle, security, logging]
  topics: [hooks, uv, tts, validation, subagents]
---

# Claude Code Hooks Mastery - Deep Analysis

## Overview

**Author**: disler
**Purpose**: Complete working implementations of all 13 Claude Code hooks with educational documentation
**Key Value**: Production-ready hook patterns with security, logging, TTS, and validation

## Repository Structure

```
.claude/
├── hooks/
│   ├── session_start.py          # 213 lines - Context loading, TTS, git status
│   ├── session_end.py            # 138 lines - Cleanup, logging
│   ├── user_prompt_submit.py     # 192 lines - Validation, agent naming
│   ├── pre_tool_use.py           # 139 lines - SECURITY BLOCKING
│   ├── post_tool_use.py          # 48 lines - Logging
│   ├── post_tool_use_failure.py  # 74 lines - Error handling
│   ├── permission_request.py     # 200 lines - Permission handling
│   ├── pre_compact.py            # 105 lines - Compression notifications
│   ├── subagent_start.py         # 163 lines - Subagent spawn
│   ├── subagent_stop.py          # 280 lines - Task summarization, TTS
│   ├── stop.py                   # 233 lines - Completion TTS, transcript export
│   ├── notification.py           # 126 lines - Async notifications
│   ├── setup.py                  # 266 lines - Hook installation/maintenance
│   ├── utils/
│   │   ├── llm/                  # LLM integrations (OpenAI, Anthropic, Ollama)
│   │   ├── tts/                  # TTS integrations (ElevenLabs, OpenAI, pyttsx3)
│   │   └── validators/           # Validation utilities
│   └── validators/
│       └── validate_file_contains.py
├── status_lines/                 # 9 versions of status lines
│   └── status_line_v1-9.py
└── data/sessions/               # Session data storage

apps/
├── server/                      # Bun + TypeScript + SQLite observability server
└── client/                      # Vue 3 real-time dashboard

ai_docs/                         # Anthropic documentation
logs/                           # Hook execution logs
specs/                          # Hook specification documents
```

## The 13 Hooks - Complete Analysis

### 1. session_start.py - Session Initialization
**Lines**: 213 | **Priority**: CRITICAL

**What it does**:
- Logs session start to `logs/session_start.json`
- Gets git status (branch, uncommitted changes)
- Fetches recent GitHub issues via `gh issue list`
- Loads context files: `.claude/CONTEXT.md`, `.claude/TODO.md`, `TODO.md`
- Optional TTS announcement ("Claude Code session started")
- Returns `additionalContext` to Claude

**Key Patterns**:
```python
# UV script header (all hooks use this)
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-dotenv"]
# ///

# Return additional context to Claude
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}
print(json.dumps(output))
```

**BB5 Application**:
- Our SessionStart hook is basic compared to this
- Should add: git status, context file loading, better logging
- The `additionalContext` feature is powerful

---

### 2. session_end.py - Cleanup
**Lines**: 138 | **Priority**: MEDIUM

**What it does**:
- Logs session end to `logs/session_end.json`
- Optional cleanup: removes `.tmp` files, stale `chat.json` (>24h)
- Logs cleanup actions to `logs/cleanup.json`

**Key Patterns**:
- Graceful error handling (always exit 0)
- Timestamped logging
- Conditional cleanup with `--cleanup` flag

---

### 3. user_prompt_submit.py - Prompt Validation
**Lines**: 192 | **Priority**: HIGH

**What it does**:
- Logs all prompts to `logs/user_prompt_submit.json`
- Manages session data in `.claude/data/sessions/{session_id}.json`
- Optional agent name generation via LLM (Ollama > Anthropic)
- Optional prompt validation (blocked patterns)
- Stores last prompt for status line

**Key Patterns**:
```python
# Block prompt with error message
print(f"Prompt blocked: {reason}", file=sys.stderr)
sys.exit(2)  # Exit code 2 = block with error

# Session data structure
session_data = {
    "session_id": session_id,
    "prompts": [],
    "agent_name": "..."  # Optional
}
```

**BB5 Application**:
- Could add prompt logging for analytics
- Agent naming is interesting for multi-agent tracking
- Validation framework for dangerous prompts

---

### 4. pre_tool_use.py - SECURITY GATE
**Lines**: 139 | **Priority**: CRITICAL

**What it does**:
- **BLOCKS dangerous `rm -rf` commands** (comprehensive pattern matching)
- **BLOCKS access to `.env` files** (but allows `.env.sample`)
- Logs all tool calls to `logs/pre_tool_use.json`

**Security Patterns**:
```python
# Comprehensive rm -rf detection
dangerous_patterns = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf
    r'\brm\s+--recursive\s+--force',
    r'\brm\s+-r\s+.*-f',
]

# Block .env file access (but not .env.sample)
if '.env' in file_path and not file_path.endswith('.env.sample'):
    return True

# Block with exit code 2
print("BLOCKED: Dangerous command detected", file=sys.stderr)
sys.exit(2)
```

**BB5 Application**:
- **IMMEDIATE**: Add this to our pre_tool_use hook
- Protects against accidental data loss
- Pattern-based blocking is extensible

---

### 5. post_tool_use.py - Tool Logging
**Lines**: 48 | **Priority**: MEDIUM

**What it does**:
- Simple logging to `logs/post_tool_use.json`

**Pattern**: Minimal hook - just logs

---

### 6. post_tool_use_failure.py - Error Handling
**Lines**: 74 | **Priority**: MEDIUM

**What it does**:
- Logs tool failures to `logs/post_tool_use_failure.json`
- Captures error details

---

### 7. permission_request.py - Permission Handling
**Lines**: 200 | **Priority**: MEDIUM

**What it does**:
- Handles permission requests (not yet in production Claude Code)
- Logging and notification

---

### 8. pre_compact.py - Compression Notifications
**Lines**: 105 | **Priority**: LOW

**What it does**:
- Notifies when context compression occurs
- Optional TTS announcement

---

### 9. subagent_start.py - Subagent Spawn
**Lines**: 163 | **Priority**: HIGH

**What it does**:
- Logs subagent spawn to `logs/subagent_start.json`
- Optional TTS announcement ("{agent_type} agent started")
- Debug logging

**Key Pattern**:
```python
# TTS priority chain
tts_priority = ["elevenlabs", "openai", "pyttsx3"]
```

---

### 10. subagent_stop.py - Subagent Completion
**Lines**: 280 | **Priority**: HIGH

**What it does**:
- **Task summarization** via LLM
- TTS lock management (prevents overlapping announcements)
- Optional TTS announcement of completion
- Logs to `logs/subagent_stop.json`

**Key Patterns**:
```python
# TTS lock to prevent overlapping
acquire_tts_lock(agent_id)
try:
    announce_completion()
finally:
    release_tts_lock(agent_id)

# Task summarization
summary = summarize_subagent_task(task_description, agent_name)
```

---

### 11. stop.py - Task Completion
**Lines**: 233 | **Priority**: HIGH

**What it does**:
- **LLM-generated completion messages** (OpenAI > Anthropic > Ollama > fallback)
- **TTS announcement** of completion
- Transcript export to `logs/chat.json`
- Logs to `logs/stop.json`

**Key Patterns**:
```python
# LLM priority chain for completion messages
llm_priority = ["openai", "anthropic", "ollama", "random_fallback"]

# TTS priority chain
tts_priority = ["elevenlabs", "openai", "pyttsx3"]
```

---

### 12. notification.py - Async Notifications
**Lines**: 126 | **Priority**: LOW

**What it does**:
- Handles async notifications
- Logging

---

### 13. setup.py - Hook Installation
**Lines**: 266 | **Priority**: MEDIUM

**What it does**:
- Hook installation and maintenance
- Permission management
- Validation

---

## Key Architectural Patterns

### 1. UV Single-File Scripts
All hooks use UV's inline script metadata:
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-dotenv"]
# ///
```

**Benefits**:
- No virtualenv needed
- Self-contained
- Fast execution
- Dependency management inline

### 2. Exit Code Semantics
- `exit 0` = Success, continue normally
- `exit 2` = Block with error message (shown to Claude)
- `exit 1` = Error (silent or logged)

### 3. JSON Logging Pattern
All hooks use the same logging pattern:
```python
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / 'hook_name.json'

# Read existing or init empty
if log_file.exists():
    with open(log_file, 'r') as f:
        log_data = json.load(f)
else:
    log_data = []

# Append and write
log_data.append(input_data)
with open(log_file, 'w') as f:
    json.dump(log_data, f, indent=2)
```

### 4. Graceful Error Handling
All hooks follow this pattern:
```python
try:
    # Main logic
    sys.exit(0)
except json.JSONDecodeError:
    sys.exit(0)  # Graceful
except Exception:
    sys.exit(0)  # Never crash Claude
```

### 5. CLI Argument Pattern
Hooks accept flags for optional features:
```python
parser = argparse.ArgumentParser()
parser.add_argument('--notify', action='store_true', help='Enable TTS')
parser.add_argument('--cleanup', action='store_true', help='Do cleanup')
args = parser.parse_args()
```

---

## Utility Libraries

### TTS System (utils/tts/)
Priority chain: ElevenLabs > OpenAI > pyttsx3 (local)

| Provider | File | Requirements |
|----------|------|--------------|
| ElevenLabs | `elevenlabs_tts.py` | ELEVENLABS_API_KEY |
| OpenAI | `openai_tts.py` | OPENAI_API_KEY |
| pyttsx3 | `pyttsx3_tts.py` | None (local) |

### LLM System (utils/llm/)
Priority chain: OpenAI > Anthropic > Ollama (local)

| Provider | File | Purpose |
|----------|------|---------|
| OpenAI | `oai.py` | Completion messages |
| Anthropic | `anth.py` | Completion messages |
| Ollama | `ollama.py` | Local LLM, agent naming |
| Task Summarizer | `task_summarizer.py` | Subagent task summaries |

---

## Extractable Assets for BB5

### IMMEDIATE IMPLEMENTATION (This Week)

1. **pre_tool_use Security Hook** (CRITICAL)
   - Block rm -rf commands
   - Block .env file access
   - Location: `.claude/hooks/pre_tool_use.py`
   - Effort: Copy-paste, test

2. **session_start Enhancement** (HIGH)
   - Add git status check
   - Load context files (.claude/CONTEXT.md, TODO.md)
   - Add structured logging
   - Effort: Adapt our existing hook

3. **JSON Logging Pattern** (HIGH)
   - Standardize all our hooks to use JSON logging
   - Location: `logs/*.json`
   - Effort: Refactor existing hooks

### SHORT TERM (This Month)

4. **TTS Integration** (MEDIUM)
   - Add audio notifications on completion
   - Priority: pyttsx3 (no API key needed)
   - Hooks: stop.py, subagent_stop.py

5. **Session Data Management** (MEDIUM)
   - Track prompts per session
   - Agent naming for multi-agent
   - Location: `.claude/data/sessions/`

6. **Status Line Versions** (LOW)
   - 9 progressive status line implementations
   - Location: `.claude/status_lines/`

### REFERENCE PATTERNS

7. **Subagent Task Summarization** (REFERENCE)
   - LLM-based summary of subagent work
   - Useful for RALF agent tracking

8. **Observability Stack** (REFERENCE)
   - Bun server + SQLite + Vue dashboard
   - Location: `apps/server/`, `apps/client/`
   - For future monitoring needs

---

## Comparison to BB5 Current Setup

| Feature | BB5 Current | Hooks Mastery | Gap |
|---------|-------------|---------------|-----|
| SessionStart | Basic | Full context loading | MEDIUM |
| PreToolUse | None | Security blocking | CRITICAL |
| Logging | Text files | JSON structured | MEDIUM |
| TTS | None | Full integration | LOW |
| Subagent tracking | None | Complete | MEDIUM |
| Status lines | Basic | 9 versions | LOW |

---

## Implementation Roadmap for BB5

### Phase 1: Security (Week 1)
- [ ] Add pre_tool_use.py with rm -rf blocking
- [ ] Add .env file protection
- [ ] Test blocking behavior

### Phase 2: Enhanced Session (Week 1-2)
- [ ] Enhance session_start.py with git status
- [ ] Add context file loading
- [ ] Add JSON logging

### Phase 3: Observability (Week 2-3)
- [ ] Convert all hooks to JSON logging
- [ ] Add session data tracking
- [ ] Create log aggregation

### Phase 4: Polish (Week 3-4)
- [ ] Add TTS for completions
- [ ] Enhance status lines
- [ ] Add subagent tracking

---

## Related Repos

- **Similar to**: Our current BB5 hooks (but more complete)
- **Complements**: awesome-claude-code (has more hook examples)
- **Contrasts with**: Continuous-Claude-v3 (framework vs hooks focus)

---

## Notes

- This is the definitive hook reference implementation
- All 13 hooks are production-ready
- UV single-file pattern is elegant
- Security blocking in pre_tool_use is essential
- TTS integration is a nice-to-have, not essential
- The logging pattern enables powerful analytics
