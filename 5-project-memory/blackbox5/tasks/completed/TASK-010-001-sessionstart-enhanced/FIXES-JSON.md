# JSON I/O Fixes for BB5 SessionStart Hook

**Task:** TASK-010-001
**Date:** 2026-02-06
**Critical Issues Fixed:** 3

---

## Summary

This document provides fixed implementations for the three critical JSON I/O issues identified in EVALUATION-AGENT-1.md:

1. **CRITICAL-004:** Wrong stdin handling (lines 59-64, 362) - Terminal detection removed, always reads JSON
2. **CRITICAL-003:** Broken JSON sanitization (lines 101, 317) - Uses `jq` for proper encoding
3. **CRITICAL-006:** Wrong JSON output format (lines 1115-1129) - `additionalContext` moved to top level

---

## Fix 1: read_stdin_input()

**Problem:** Terminal detection logic (`[ -t 0 ]`) incorrectly assumes terminal = no input. Claude Code ALWAYS provides JSON on stdin, even in terminal. The `-n` flag reads characters, not bytes, causing UTF-8 corruption.

**Solution:** Remove terminal detection, always attempt to read JSON. Use proper byte counting with `-N` flag.

```bash
# Maximum input size (1MB to prevent memory exhaustion)
readonly MAX_INPUT_SIZE=1048576
# Timeout for stdin reading (5 seconds)
readonly STDIN_TIMEOUT=5

read_stdin_input() {
    local input=""
    local original_lang="${LANG:-}"

    # Set C locale for consistent behavior
    export LANG=C

    # Always read from stdin - Claude Code ALWAYS provides JSON
    # Use -N for bytes (not -n for characters) to handle UTF-8 correctly
    if IFS= read -r -t "$STDIN_TIMEOUT" -N "$MAX_INPUT_SIZE" input 2>/dev/null; then
        # Validate JSON using jq
        if [ -n "$input" ] && echo "$input" | jq -e . >/dev/null 2>&1; then
            export LANG="$original_lang"
            echo "$input"
            return 0
        fi
    fi

    # Return empty JSON on any failure (timeout, invalid JSON, no input)
    export LANG="$original_lang"
    echo "{}"
    return 0
}
```

**Key Changes:**
- Removed `[ -t 0 ]` terminal detection
- Changed `-n` to `-N` for proper byte counting (fixes UTF-8 corruption)
- Always attempts to read stdin
- Returns `{}` on any failure condition

---

## Fix 2: sanitize_for_json()

**Problem:** Uses `tr` and `sed` which destroy JSON structure, don't handle control characters, and have BSD/GNU compatibility issues.

**Solution:** Use `jq` for proper JSON string encoding.

```bash
sanitize_for_json() {
    local input="$1"

    # Use jq for proper JSON string encoding
    # This handles: quotes, backslashes, newlines, tabs, control chars
    if command -v jq >/dev/null 2>&1; then
        printf '%s' "$input" | jq -Rs '.' | sed 's/^"//;s/"$//'
    else
        # Fallback: basic escaping (not recommended for production)
        # Only handles minimal cases - jq is REQUIRED for proper operation
        printf '%s' "$input" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g; s/\n/\\n/g; s/\r/\\r/g'
    fi
}
```

**Key Changes:**
- Uses `jq -Rs '.'` for proper JSON string encoding
- Handles all control characters (\\b, \\f, \\n, \\r, \\t)
- Removes surrounding quotes added by jq
- Includes fallback with warning (jq is REQUIRED)

**Alternative Implementation (if jq must be checked at startup):**

```bash
# Add to startup checks in main():
check_dependencies() {
    if ! command -v jq >/dev/null 2>&1; then
        log_error "jq is required but not installed"
        return 1
    fi
    return 0
}

# Then sanitize_for_json becomes:
sanitize_for_json() {
    local input="$1"
    # jq -Rs reads raw, outputs as JSON string with quotes
    # sed removes the surrounding quotes for embedding in JSON value
    printf '%s' "$input" | jq -Rs '.' | sed 's/^"//;s/"$//'
}
```

---

## Fix 3: generate_json_output()

**Problem:** `additionalContext` is nested inside `hookSpecificOutput`, but Claude Code expects it at the TOP LEVEL.

**Solution:** Move `additionalContext` to top level, keep `hookSpecificOutput` for hook-specific data.

```bash
generate_json_output() {
    local project="$1"
    local agent_type="$2"
    local mode="$3"
    local run_dir="$4"
    local run_id="$5"

    # Build context message
    local context
    context="BB5 Session Initialized | Project: $project | Agent: $agent_type | Mode: $mode | Run: $run_id"

    if [ ${#ERRORS[@]} -gt 0 ]; then
        context="$context | Warnings: ${#ERRORS[@]}"
    fi

    # Generate JSON using jq for proper structure
    # Claude Code expects: {"additionalContext": "...", "hookSpecificOutput": {...}}
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

**Key Changes:**
- `additionalContext` is now at TOP LEVEL (not nested)
- Uses `jq -n` to build proper JSON structure
- No manual string sanitization needed (jq handles it)
- Output is guaranteed valid JSON

**Alternative (if jq not available for output generation):**

```bash
generate_json_output() {
    local project="$1"
    local agent_type="$2"
    local mode="$3"
    local run_dir="$4"
    local run_id="$5"

    # Build context message
    local context
    context="BB5 Session Initialized | Project: $project | Agent: $agent_type | Mode: $mode | Run: $run_id"

    if [ ${#ERRORS[@]} -gt 0 ]; then
        context="$context | Warnings: ${#ERRORS[@]}"
    fi

    # Sanitize context for JSON embedding
    local sanitized_context
    sanitized_context=$(sanitize_for_json "$context")

    # Output valid JSON with additionalContext at TOP LEVEL
    # This is the Claude Code expected format
    cat << EOF
{
  "additionalContext": "$sanitized_context",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "project": "$project",
    "agentType": "$agent_type",
    "mode": "$mode",
    "runDir": "$run_dir",
    "runId": "$run_id",
    "hookVersion": "$HOOK_VERSION",
    "timestamp": "$(date -Iseconds)"
  }
}
EOF
}
```

---

## Complete Fixed Section (Lines 349-374, 316-318, 1095-1130)

Replace the three functions in the specification with:

```bash
# =============================================================================
# STDIN INPUT HANDLING
# =============================================================================

read_stdin_input() {
    local input=""
    local original_lang="${LANG:-}"

    # Set C locale for consistent behavior
    export LANG=C

    # Always read from stdin - Claude Code ALWAYS provides JSON
    # Use -N for bytes (not -n for characters) to handle UTF-8 correctly
    if IFS= read -r -t "$STDIN_TIMEOUT" -N "$MAX_INPUT_SIZE" input 2>/dev/null; then
        # Validate JSON using jq
        if [ -n "$input" ] && echo "$input" | jq -e . >/dev/null 2>&1; then
            export LANG="$original_lang"
            echo "$input"
            return 0
        fi
    fi

    # Return empty JSON on any failure (timeout, invalid JSON, no input)
    export LANG="$original_lang"
    echo "{}"
    return 0
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

sanitize_for_json() {
    local input="$1"
    # Use jq for proper JSON string encoding
    # jq -Rs reads raw, outputs as JSON string with quotes
    # sed removes the surrounding quotes for embedding in JSON value
    printf '%s' "$input" | jq -Rs '.' | sed 's/^"//;s/"$//'
}

# =============================================================================
# JSON OUTPUT GENERATION
# =============================================================================

generate_json_output() {
    local project="$1"
    local agent_type="$2"
    local mode="$3"
    local run_dir="$4"
    local run_id="$5"

    # Build context message
    local context
    context="BB5 Session Initialized | Project: $project | Agent: $agent_type | Mode: $mode | Run: $run_id"

    if [ ${#ERRORS[@]} -gt 0 ]; then
        context="$context | Warnings: ${#ERRORS[@]}"
    fi

    # Generate JSON using jq for proper structure
    # Claude Code expects: {"additionalContext": "...", "hookSpecificOutput": {...}}
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

---

## Validation

Test the fixed functions:

```bash
# Test 1: read_stdin_input with valid JSON
echo '{"test": "value"}' | read_stdin_input
# Expected: {"test": "value"}

# Test 2: read_stdin_input with no input
read_stdin_input </dev/null
# Expected: {}

# Test 3: sanitize_for_json with special chars
sanitize_for_json 'Line 1
Line 2	Tabbed "quoted" and \backslash\'
# Expected: Line 1\nLine 2\tTabbed \"quoted\" and \\backslash\\

# Test 4: generate_json_output structure
ERRORS=()
generate_json_output "blackbox5" "planner" "autonomous" "/tmp/run" "run-001"
# Expected: Valid JSON with additionalContext at TOP LEVEL
```

---

## Files Modified

- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks/active/TASK-010-001-sessionstart-enhanced/SPECIFICATION.md`
  - Lines 349-374: `read_stdin_input()` function
  - Lines 316-318: `sanitize_for_json()` function
  - Lines 1095-1130: `generate_json_output()` function

---

*Fixes applied by Claude Code - 2026-02-06*
