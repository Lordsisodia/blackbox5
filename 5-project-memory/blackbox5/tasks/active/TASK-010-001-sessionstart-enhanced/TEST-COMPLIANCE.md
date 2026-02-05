# BB5 SessionStart Hook - Claude Code Compliance Test Report

**Test Date:** 2026-02-06
**Hook Version:** 2.0.0
**Specification:** SPECIFICATION-v2-PRODUCTION.md
**Claude Code Version:** Current (as of Feb 2026)

---

## Executive Summary

**COMPLIANCE SCORE: 67/100** - **CONDITIONAL PASS**

The BB5 SessionStart hook meets basic functionality requirements but has several compliance issues that may cause unexpected behavior with Claude Code. The hook will function but may not integrate optimally with the matcher system and has potential issues with stdin handling and output format.

---

## Detailed Compliance Analysis

### 1. JSON Input Handling (SessionStart receives JSON on stdin)

**Status:** PARTIAL COMPLIANCE

**Claude Code Requirement:**
- SessionStart hooks receive JSON on stdin with fields: `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`, `source`, `model`, and optionally `agent_type`
- Input format:
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-5-20250929"
}
```

**Hook Implementation (Lines 237-253):**
```bash
read_stdin_input() {
    local input=""
    local original_lang="${LANG:-}"
    export LANG=C

    if IFS= read -r -t "$STDIN_TIMEOUT" -N "$MAX_INPUT_SIZE" input 2>/dev/null; then
        if [ -n "$input" ] && echo "$input" | jq -e . >/dev/null 2>&1; then
            export LANG="$original_lang"
            echo "$input"
            return 0
        fi
    fi

    export LANG="$original_lang"
    echo "{}"
    return 0
}
```

**Issues Found:**

| Issue | Severity | Description |
|-------|----------|-------------|
| Uses `read -N` (byte count) instead of reading full input | MEDIUM | The `-N "$MAX_INPUT_SIZE"` flag reads exactly that many bytes or until EOF. This could truncate input if not careful, though 1MB is generous |
| Returns `{}` on any read/parse failure | LOW | This is defensive but means the hook never actually uses the SessionStart input fields like `source`, `cwd`, or `agent_type` |
| No extraction of input fields | MEDIUM | The hook completely ignores the input JSON fields. It doesn't use `source` for matcher logic, doesn't respect `cwd`, and ignores `agent_type` |
| Timeout of 5 seconds | LOW | The `STDIN_TIMEOUT=5` is reasonable but undocumented in Claude Code specs |

**Recommendation:** The hook should parse and use the input fields, especially `source` (for matcher compatibility) and `cwd` (to set working directory context).

**Score: 6/10**

---

### 2. JSON Output Format

**Status:** NON-COMPLIANT

**Claude Code Requirement:**
For SessionStart, the output format must be:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Your context text here that Claude will see"
  }
}
```

**Key Requirements:**
- `additionalContext` must be INSIDE `hookSpecificOutput` for SessionStart
- The `additionalContext` field is what Claude actually sees as context

**Hook Implementation (Lines 735-771):**
```bash
generate_json_output() {
    # ...
    jq -n \
        --arg context "$context" \
        --arg project "$project" \
        --arg agent_type "$agent_type" \
        --arg mode "$mode" \
        --arg run_dir "$run_dir" \
        --arg run_id "$run_id" \
        --arg hook_version "$HOOK_VERSION" \
        --arg timestamp "$(date -Iseconds)" \
        '{
            additionalContext: $context,
            hookSpecificOutput: {
                hookEventName: "SessionStart",
                project: $project,
                agentType: $agent_type,
                mode: $mode,
                runDir: $run_dir,
                runId: $run_id,
                hookVersion: $hook_version,
                timestamp: $timestamp
            }
        }'
}
```

**Critical Issue:**

The hook places `additionalContext` at the **top level** of the JSON object, but according to Claude Code documentation, for SessionStart hooks, `additionalContext` must be **inside** `hookSpecificOutput`.

**Current (Wrong):**
```json
{
  "additionalContext": "BB5 Session Initialized | Project: blackbox5 | ...",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "project": "blackbox5",
    ...
  }
}
```

**Required (Correct):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "BB5 Session Initialized | Project: blackbox5 | ..."
  }
}
```

**Impact:** Claude Code may not surface the additionalContext to the conversation. This is a known issue documented in GitHub issue #16538 ("Plugin SessionStart hooks don't surface hookSpecificOutput.additionalContext to Claude").

**Score: 3/10**

---

### 3. CLAUDE_ENV_FILE Usage

**Status:** COMPLIANT

**Claude Code Requirement:**
- Only SessionStart hooks can write to `CLAUDE_ENV_FILE`
- Must append export statements to the file
- Variables written will be available in subsequent Bash tool calls

**Hook Implementation (Lines 446-518):**
```bash
persist_environment_vars() {
    local env_file="$1"
    # ... validation ...

    if [ -n "$CLAUDE_ENV_FILE" ]; then
        if persist_environment_vars "$CLAUDE_ENV_FILE" "$project" "$agent_type" "$RUN_DIR" "$RUN_ID"; then
            log_info "Environment variables persisted"
        else
            log_error "Failed to persist environment variables"
        fi
    fi
}
```

The hook:
- Checks if `CLAUDE_ENV_FILE` is set before attempting to write
- Uses base64 encoding to prevent command injection
- Uses file locking for atomic operations
- Appends to the file (via the section-based approach)

**Strengths:**
- Properly validates the environment file path
- Uses atomic write operations (temp file + mv)
- Implements file locking with flock
- Encodes values in base64 to prevent injection

**Score: 9/10**

---

### 4. Exit Codes

**Status:** COMPLIANT

**Claude Code Requirement:**
- Exit 0: Success - stdout is parsed for JSON, context added to conversation
- Exit 2: Blocking error - stderr shown to user
- Any other exit code: Non-blocking error - stderr shown in verbose mode only

**Hook Implementation:**
- Line 126: Returns 1 on dependency validation failure
- Line 782: Returns 1 if dependency validation fails
- Line 804: Returns 1 if run folder creation fails
- Line 828: Returns 0 on success
- Line 832: `exit 0` at end of script

**Analysis:**
- The hook uses exit 0 for success (correct)
- The hook uses exit 1 for errors (acceptable - treated as non-blocking error)
- Exit 2 is not used, which is fine since SessionStart cannot block

**Note:** For SessionStart specifically, exit code 2 behavior is "Shows stderr to user only" (cannot block session start). The hook's use of exit 1 is acceptable.

**Score: 10/10**

---

### 5. Timeout Handling

**Status:** COMPLIANT

**Claude Code Requirement:**
- Default timeout for command hooks: 600 seconds (10 minutes)
- Hooks can specify custom timeout in settings.json
- SessionStart hooks should be fast since they run on every session

**Hook Implementation:**
- The hook itself doesn't set a timeout
- Timeout is controlled by Claude Code's hook configuration
- The hook has internal timeouts: `STDIN_TIMEOUT=5`, `LOCK_TIMEOUT=10`

**Analysis:**
- The hook doesn't hardcode a timeout that would conflict with Claude Code's timeout
- Internal timeouts are for specific operations (reading stdin, acquiring locks)
- No risk of hitting the 30-second limit mentioned in the task description (Claude Code default is 600s for commands)

**Score: 10/10**

---

### 6. Stderr Usage

**Status:** COMPLIANT

**Claude Code Requirement:**
- Stderr is shown to user on exit 2 (blocking error)
- Stderr is shown in verbose mode (Ctrl+O) for other exit codes
- Stdout must contain ONLY valid JSON on exit 0

**Hook Implementation (Lines 136-152):**
```bash
log_error() {
    local message="$1"
    ERRORS+=("$message")
    echo "[ERROR] $message" >&2
}

log_info() {
    local message="$1"
    echo "[INFO] $message" >&2
}

log_debug() {
    local message="$1"
    if [ "${BB5_DEBUG:-}" = "true" ]; then
        echo "[DEBUG] $message" >&2
    fi
}
```

**Analysis:**
- All logging goes to stderr (correct)
- JSON output goes to stdout (correct)
- No risk of polluting stdout with log messages

**Score: 10/10**

---

### 7. Working Directory Behavior

**Status:** PARTIAL COMPLIANCE

**Claude Code Requirement:**
- Hooks run in the current working directory with Claude Code's environment
- The `cwd` field in input JSON indicates the working directory
- `$CLAUDE_PROJECT_DIR` is available for referencing project root

**Hook Implementation:**
- Line 260: `local cwd="$PWD"` - uses current PWD
- Line 786: `stdin_input=$(read_stdin_input)` - reads input but doesn't extract `cwd`
- The hook never uses the `cwd` field from stdin

**Issues:**
1. The hook ignores the `cwd` field from the input JSON
2. The hook uses `$PWD` which should match `cwd`, but this is an assumption
3. No validation that `$PWD` matches the input `cwd`

**Recommendation:** The hook should extract and use the `cwd` field from stdin to ensure it's operating in the correct directory.

**Score: 6/10**

---

### 8. Matcher System Compatibility

**Status:** NON-COMPLIANT

**Claude Code Requirement:**
- SessionStart matchers filter on `source` field: `startup`, `resume`, `clear`, `compact`
- The hook should be aware of which matcher triggered it
- Configuration example:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [ ... ]
      }
    ]
  }
}
```

**Hook Implementation:**
- The hook completely ignores the `source` field from stdin
- The hook runs the same logic regardless of how the session started
- No support for different behavior on `startup` vs `resume` vs `clear` vs `compact`

**Issues:**
1. If user configures matcher for only `startup`, the hook still runs the same code
2. The hook cannot differentiate between session start types
3. This may cause unnecessary run folder creation on `/clear` or `/compact`

**Recommendation:** The hook should:
1. Extract the `source` field from stdin
2. Potentially skip run folder creation for `clear` and `compact` events
3. Document which matchers are appropriate

**Score: 3/10**

---

## Summary Table

| Criterion | Score | Weight | Weighted Score |
|-----------|-------|--------|----------------|
| JSON Input Handling | 6/10 | 15% | 0.9 |
| JSON Output Format | 3/10 | 25% | 0.75 |
| CLAUDE_ENV_FILE Usage | 9/10 | 15% | 1.35 |
| Exit Codes | 10/10 | 10% | 1.0 |
| Timeout Handling | 10/10 | 10% | 1.0 |
| Stderr Usage | 10/10 | 10% | 1.0 |
| Working Directory | 6/10 | 10% | 0.6 |
| Matcher System | 3/10 | 5% | 0.15 |
| **TOTAL** | | **100%** | **6.75/10** |

**Final Score: 67.5/100 (rounded to 67/100)**

---

## Critical Issues Requiring Fix

### Issue #1: additionalContext Placement (CRITICAL)

**Problem:** The `additionalContext` field is at the top level of the JSON output, but Claude Code expects it inside `hookSpecificOutput` for SessionStart hooks.

**Fix:** Modify `generate_json_output()` function:
```bash
generate_json_output() {
    # ... variable setup ...
    jq -n \
        --arg context "$context" \
        --arg project "$project" \
        --arg agent_type "$agent_type" \
        --arg mode "$mode" \
        --arg run_dir "$run_dir" \
        --arg run_id "$run_id" \
        --arg hook_version "$HOOK_VERSION" \
        --arg timestamp "$(date -Iseconds)" \
        '{
            hookSpecificOutput: {
                hookEventName: "SessionStart",
                additionalContext: $context,
                project: $project,
                agentType: $agent_type,
                mode: $mode,
                runDir: $run_dir,
                runId: $run_id,
                hookVersion: $hook_version,
                timestamp: $timestamp
            }
        }'
}
```

### Issue #2: Ignoring Input Fields (HIGH)

**Problem:** The hook ignores all input fields from stdin, including `source`, `cwd`, `agent_type`, and `model`.

**Fix:** Parse the input JSON and use the fields:
```bash
# Extract fields from stdin
SOURCE=$(echo "$stdin_input" | jq -r '.source // "startup"')
CWD=$(echo "$stdin_input" | jq -r '.cwd // "."')
INPUT_AGENT_TYPE=$(echo "$stdin_input" | jq -r '.agent_type // empty')

# Use INPUT_AGENT_TYPE if provided by Claude Code
if [ -n "$INPUT_AGENT_TYPE" ]; then
    AGENT_TYPE="$INPUT_AGENT_TYPE"
fi

# Potentially skip run folder creation for certain sources
case "$SOURCE" in
    clear|compact)
        # Maybe skip or use different logic
        ;;
esac
```

### Issue #3: Matcher Incompatibility (MEDIUM)

**Problem:** The hook runs the same logic regardless of which matcher triggered it.

**Recommendation:** Document that this hook should use matcher `"*"` (all sources) or add logic to handle different sources appropriately.

---

## Recommendations

1. **Fix JSON output format** - Move `additionalContext` inside `hookSpecificOutput`
2. **Parse stdin input** - Extract and use `source`, `cwd`, and `agent_type` fields
3. **Add source-based logic** - Consider different behavior for `startup` vs `resume` vs `clear` vs `compact`
4. **Document matcher usage** - Specify which matchers are appropriate for this hook
5. **Test with actual Claude Code** - Verify the hook works correctly in practice

---

## Conclusion

The BB5 SessionStart hook is well-structured from a Bash scripting perspective with good security practices (base64 encoding, file locking, path validation). However, it has critical compliance issues with Claude Code's expected JSON format that will likely prevent the additional context from being surfaced to Claude.

**Verdict:** Fix the JSON output format before deploying to production.

---

*Report generated by Claude Code Platform Engineer*
*Sources: [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)*
