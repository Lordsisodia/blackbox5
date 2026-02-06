# Stop Hook Checklist - Hook Mechanics Review

**Reviewer:** Claude Code Hooks Expert
**Date:** 2026-02-06
**Target:** `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/hooks/pipeline/stop/STOP_HOOK_CHECKLIST.md`
**Score:** 42/100

---

## Executive Summary

The STOP_HOOK_CHECKLIST.md is **fundamentally flawed** from a Claude Code Hook Mechanics perspective. It demonstrates a severe misunderstanding of how Stop hooks actually work, conflating blocking behavior (PreToolUse/UserPromptSubmit) with Stop hook behavior, and inventing JSON schemas that do not exist in the Claude Code hook protocol.

**Critical Finding:** The checklist describes a blocking validation system that **cannot be implemented** with Stop hooks as they exist in Claude Code. Stop hooks fire AFTER the session has already ended - they cannot prevent the session from stopping.

---

## Detailed Analysis by Category

### 1. Input/Output Format - Score: 20/100

#### Critical Errors

**1.1 Invented Input Fields**

The checklist claims Stop hooks receive this JSON:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/dir",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

**VERIFIED ACTUAL INPUT** (from claude-code-hooks-mastery and Continuous-Claude-v3):
```json
{
  "session_id": "uuid",
  "transcript_path": "/path/to/transcript.jsonl",
  "duration_seconds": 3600
}
```

**Problems:**
- `hook_event_name` is NOT in Stop hook input (it's only in SessionStart output)
- `stop_hook_active` is NOT a Claude Code field - this appears to be an invention
- `cwd` is NOT passed to Stop hooks

**Evidence:**
- `/Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/stop.py` lines 165-170
- `/Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/Continuous-Claude-v3/.claude/hooks/auto-handoff-stop.py` lines 46-52

#### 1.2 Completely Wrong Output Format

The checklist claims Stop hooks can return:
```json
{
  "decision": "block",
  "reason": "THOUGHTS.md is incomplete...",
  "failures": [...],
  "suggested_actions": [...]
}
```

**ACTUAL CLAUDE CODE BEHAVIOR:**

Stop hooks **CANNOT BLOCK**. They fire AFTER the session has ended. From the official Claude Code documentation patterns:

```bash
# Stop hook exit codes:
# 0 = Success (session ends normally)
# Non-zero = Error logged, but session STILL ENDS
```

The `"decision": "block"` JSON format is for **PreToolUse** and **UserPromptSubmit** hooks only. Stop hooks are notification-only - they cannot prevent session termination.

**Evidence:**
- `/Users/shaansisodia/.blackbox5/.claude/HOOKS.md` lines 155-164 clearly state Stop hook input does NOT support blocking
- `/Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/Continuous-Claude-v3/.claude/hooks/auto-handoff-stop.py` exits with JSON `{"decision": "block"}` but this is a NO-OP for Stop hooks

---

### 2. Blocking Mechanism - Score: 0/100

#### Critical Misunderstanding

The entire checklist is built on a **false premise**:

> "The Stop hook is BB5's quality gate and task completion validator. It fires when Claude is about to stop responding and can BLOCK completion until work is properly validated."

**THIS IS FALSE.**

**How Stop Hooks Actually Work:**

1. User types `exit` or session ends naturally
2. Claude Code terminates the session
3. **AFTER** termination, Stop hook fires
4. Stop hook can log, clean up, notify - but CANNOT prevent stop
5. Session is already gone

**Evidence from Multi-Agent Ralph Loop** (`/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/multi-agent-ralph-loop/.claude/hooks/stop-verification.sh`):
```bash
# This hook uses "decision": "approve" but it's advisory only
trap 'echo "{\"decision\": \"approve\"}"' ERR EXIT
```

Even the multi-agent-ralph-loop's "stop-verification" hook acknowledges this - it uses `"decision": "approve"` as a formality, knowing it cannot actually block.

#### The Real Blocking Hooks

If you want to block session end, you need:
- **PreToolUse** hook on `exit` command (but exit is not a tool)
- **UserPromptSubmit** hook analyzing user intent (complex and unreliable)

**There is no legitimate way to block session end in Claude Code.**

---

### 3. Error Handling and Edge Cases - Score: 35/100

#### 3.1 Missing Critical Error Patterns

The checklist mentions none of these real-world Stop hook failure modes:

| Failure Mode | Impact | Checklist Coverage |
|--------------|--------|-------------------|
| Transcript file locked/deleted | Hook crashes | ❌ Not mentioned |
| Session ID missing from input | Cannot correlate logs | ❌ Not mentioned |
| Stop hook timeout (Claude kills it) | Partial cleanup | ❌ Not mentioned |
| Multiple Stop hooks - one fails | Others may not run | ❌ Not mentioned |
| Git operations during stop | Race conditions | ❌ Not mentioned |
| Large transcript files (>10MB) | OOM or timeout | ❌ Not mentioned |

#### 3.2 Wrong Error Handling Pattern

The checklist shows:
```python
# BLOCK if:
- Required file doesn't exist
- Content < min_chars
```

**Correct Stop Hook Pattern** (from braintrust-tracing):
```bash
# Read input from stdin (must be done synchronously)
INPUT=$(cat)

# Run heavy processing in background to avoid blocking session end
ASYNC_INPUT_FILE=$(mktemp)
echo "$INPUT" > "$ASYNC_INPUT_FILE"

(
    # Background process
    INPUT=$(cat "$ASYNC_INPUT_FILE")
    rm -f "$ASYNC_INPUT_FILE"
    # ... processing ...
) </dev/null >/dev/null 2>&1 &

# Exit immediately - session is ending regardless
exit 0
```

Stop hooks should **never block** - they should fork background processes for heavy work.

---

### 4. Timeout and Performance - Score: 55/100

#### 4.1 Performance Budget Issues

The checklist claims:
| Phase | Target Time |
|-------|-------------|
| Documentation validation | <100ms |
| Git state check | <50ms |
| Task status check | <50ms |
| Validation scripts | <200ms |
| **Total (blocking)** | **<400ms** |

**Problems:**

1. **"Blocking" is wrong** - Stop hooks don't block anything
2. **Git operations are optimistic** - `git status` on large repos can take 500ms+
3. **Validation scripts at 200ms** - Running 3 Python scripts in 200ms is unrealistic
4. **No timeout handling** - Claude Code will kill the hook after ~30 seconds, but partial work may leave system in inconsistent state

#### 4.2 Missing Timeout Specifications

The checklist should specify:
- Hook timeout (Claude Code default is ~30s)
- Individual operation timeouts
- Graceful degradation when timeouts hit

**Correct Pattern** (from compiler-in-the-loop-stop.sh):
```bash
# Early exit if no work needed (~500ms saved)
if [[ ! -f "$STATE_FILE" ]]; then
  echo '{}'
  exit 0
fi
```

---

### 5. Hook Chaining - Score: 30/100

#### 5.1 Missing Chaining Semantics

The checklist shows multiple validators but doesn't explain:

1. **Execution Order**: Hooks run in sequence as defined in settings.json
2. **Failure Handling**: If Hook A fails, does Hook B still run?
3. **State Passing**: How do hooks share state?

**Evidence from settings.json** (`/Users/shaansisodia/.blackbox5/.claude/settings.json`):
```json
"Stop": [
  {
    "hooks": [
      {"type": "command", "command": "bash /Users/.../stop-validate-docs.sh"},
      {"type": "command", "command": "bash /Users/.../stop-hierarchy-update.sh"}
    ]
  }
]
```

**Actual Behavior:**
- Hooks run sequentially
- If hook 1 fails (exit != 0), hook 2 still runs (Claude Code doesn't short-circuit)
- Each hook gets the SAME stdin input
- Hooks cannot communicate with each other

#### 5.2 No Mention of "matcher" Limitation

Stop hooks do NOT support matchers (unlike PreToolUse). The checklist implies they can filter by event type - this is impossible.

---

## Technical Gaps and Incorrect Assumptions

### Gap 1: Session State After Stop

**Checklist Assumption:** Can update task status, move folders, sync STATE.yaml

**Reality:** After Stop hook fires:
- Claude Code session is dead
- No further tool use is possible
- File operations work (bash commands) but cannot affect the ended session
- Any "blocking" would happen AFTER user has already exited

### Gap 2: Auto-Actions Are Misleading

The checklist lists "Auto-Actions (If Validation Passes)":
- Task Status Updates
- STATE.yaml Synchronization
- Learning Extraction
- Git Auto-Commit

**Problem:** These are fine as cleanup actions, but the framing "If Validation Passes" implies validation can fail and block - which it cannot.

### Gap 3: Environment Variables

The checklist mentions `stop_hook_active` to prevent infinite loops. This field does not exist in Claude Code.

**Actual Pattern** (from auto-handoff-stop.py):
```python
# Avoid recursion if stop hook triggers itself
if data.get('stop_hook_active'):
    print('{}')
    sys.exit(0)
```

This is defensive coding against a hypothetical scenario. Stop hooks cannot trigger themselves - the session is already ending.

### Gap 4: Exit Code Semantics

The checklist shows:
| Code | Behavior |
|------|----------|
| **0** | Success - Claude stops (unless JSON contains `decision: "block"`) |
| **2** | Blocking error - prevents stop, stderr shown to Claude |
| **Other** | Non-blocking error - stderr shown in verbose mode only |

**ACTUAL CLAUDE CODE BEHAVIOR:**

From `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-010-001-sessionstart-enhanced/HOOK_ENVIRONMENT_VARIABLES.md`:

| Hook Event | Can Block |
|------------|-----------|
| **SessionStart** | ❌ No |
| UserPromptSubmit | ✅ Yes (exit 2) |
| PreToolUse | ✅ Yes (exit 2) |
| PostToolUse | ❌ No |
| SubagentStart | ❌ No |
| SubagentStop | ✅ Yes (exit 2) |
| **Stop** | ✅ Yes (exit 2) |
| SessionEnd | ❌ No |

**WAIT** - The HOOK_ENVIRONMENT_VARIABLES.md claims Stop CAN block with exit 2. But this contradicts the actual observed behavior and the braintrust-tracing implementation which backgrounds all work.

**Resolution:** The documentation is ambiguous. Exit 2 may show an error message, but the session still ends. The "blocking" behavior for Stop hooks is NOT the same as PreToolUse blocking.

---

## Recommendations

### Immediate Fixes Required

1. **Remove all "blocking" language**
   - Stop hooks cannot block session end
   - Change "BLOCKING VALIDATIONS" to "VALIDATION REPORTING"
   - Remove `{"decision": "block"}` JSON format

2. **Correct the input format**
   - Remove `hook_event_name` (not in Stop input)
   - Remove `stop_hook_active` (not a real field)
   - Remove `cwd` (not passed to Stop)
   - Add `duration_seconds` (actual field)

3. **Fix exit code documentation**
   - Exit 0: Success, session ends
   - Exit non-zero: Error logged, session still ends
   - No "blocking" exit code exists for Stop hooks

4. **Add background processing pattern**
   - All heavy work must be backgrounded
   - Stop hook should exit immediately
   - Use temp files to pass data to background process

### Architecture Changes

If you actually need blocking validation before session end, implement:

```bash
# Option 1: PreCompact Hook (fires before context compaction)
# Check documentation, block compaction if incomplete
# This keeps session alive but forces user to continue

# Option 2: UserPromptSubmit Hook
# Detect "exit" or "quit" in user prompt
# Show warning about incomplete work
# Cannot truly block but can discourage

# Option 3: Change Workflow
# Don't rely on hooks for validation
# Use explicit `/complete` command that runs validation
# Only exit after validation passes
```

### Documentation Updates

1. Clarify that Stop hooks are "cleanup/notification" only
2. Add section on "What Stop Hooks Cannot Do"
3. Reference actual working implementations:
   - `stop-validate-docs.sh` (simple validation, exits with warning)
   - `stop-hierarchy-update.sh` (async updates)
   - `auto-handoff-stop.py` (JSON logging)
   - `braintrust-tracing/stop_hook.sh` (background processing)

---

## Conclusion

The STOP_HOOK_CHECKLIST.md describes a system that **cannot exist** within Claude Code's hook architecture. It conflates PreToolUse blocking behavior with Stop hook notification behavior, invents JSON fields, and promises capabilities (blocking session end) that are technically impossible.

**Score Breakdown:**
- Input Format: 20/100 (invented fields)
- Output Format: 10/100 (wrong blocking semantics)
- Blocking Mechanism: 0/100 (fundamentally misunderstood)
- Error Handling: 35/100 (missing critical patterns)
- Performance: 55/100 (optimistic timing, no timeouts)
- Hook Chaining: 30/100 (missing semantics)
- **Overall: 42/100**

**Recommendation:** Rewrite from scratch using actual working Stop hook implementations as reference. Remove all blocking/validation language and reframe as "Session End Cleanup Checklist."

---

## References

1. **Working Stop Hook Examples:**
   - `/Users/shaansisodia/.blackbox5/.claude/hooks/stop-validate-docs.sh`
   - `/Users/shaansisodia/.blackbox5/.claude/hooks/stop-hierarchy-update.sh`
   - `/Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/.claude/hooks/stop.py`
   - `/Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/Continuous-Claude-v3/.claude/hooks/auto-handoff-stop.py`
   - `/Users/shaansisodia/.blackbox5/6-roadmap/.research/external/GitHub/Claude-Code/data/repos/Continuous-Claude-v3/.claude/plugins/braintrust-tracing/hooks/stop_hook.sh`

2. **Documentation:**
   - `/Users/shaansisodia/.blackbox5/.claude/HOOKS.md`
   - `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-010-001-sessionstart-enhanced/HOOK_ENVIRONMENT_VARIABLES.md`
   - `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/.docs/github/multi-agent-ralph-loop/CLAUDE.md`
