# BB5 SessionStart Hook - Improvement Analysis

**Agent:** DevOps Engineer / Shell Scripting Specialist
**Date:** 2026-02-06
**Task:** TASK-010-001
**Quality Rating:** 92/100 (Current) → Target: 98/100

---

## Executive Summary

The SessionStart hook specification is well-designed and production-ready at 92/100. However, there are several areas for improvement based on:
- Claude Code official hooks documentation
- Google Shell Style Guide
- POSIX compliance standards
- ShellCheck best practices
- Comparison with existing hook implementations in the codebase

**Total Improvements Identified:** 18
**Critical:** 3 | **High:** 5 | **Medium:** 7 | **Low:** 3

---

## 1. MISSING FEATURES

### 1.1 Health Check / Dependency Validation
**Problem:** Hook assumes all dependencies (jq, flock, git) are available without verification.

**Current State:**
```bash
# No dependency checking before use
if echo "$input" | jq -e . >/dev/null 2>&1; then
```

**Suggested Code:**
```bash
# At start of main() or in a validate_dependencies() function
validate_dependencies() {
    local missing_deps=()

    # Core dependencies
    if ! command -v jq >/dev/null 2>&1; then
        missing_deps+=("jq")
    fi

    if ! command -v flock >/dev/null 2>&1; then
        missing_deps+=("flock")
    fi

    if ! command -v git >/dev/null 2>&1; then
        missing_deps+=("git")
    fi

    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        # Output valid JSON even on failure
        cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "ERROR: Missing dependencies: ${missing_deps[*]}",
    "project": "unknown",
    "agentType": "unknown",
    "mode": "manual",
    "runDir": "$(pwd)",
    "runId": "error-$(date +%s)",
    "hookVersion": "$HOOK_VERSION",
    "timestamp": "$(date -Iseconds)"
  }
}
EOF
        return 1
    fi
}
```

**Impact:** Critical
**Effort:** Easy
**Rationale:** Hook could fail silently or produce invalid JSON if dependencies missing.

---

### 1.2 Configuration File Support
**Problem:** All configuration is hardcoded as readonly variables. No user customization without editing the script.

**Current State:**
```bash
readonly MAX_INPUT_SIZE=1048576  # 1MB
readonly STDIN_TIMEOUT=5
readonly LOCK_TIMEOUT=10
```

**Suggested Code:**
```bash
# Load configuration from file if exists
load_config() {
    local config_file="${BB5_CONFIG_FILE:-$HOME/.blackbox5/hook-config.yaml}"

    # Default values
    MAX_INPUT_SIZE=1048576
    STDIN_TIMEOUT=5
    LOCK_TIMEOUT=10
    DEBUG_MODE=false

    # Override from config file if exists
    if [ -f "$config_file" ]; then
        # Parse YAML values (simplified - could use yq if available)
        local config_max_size
        config_max_size=$(grep "max_input_size:" "$config_file" 2>/dev/null | cut -d':' -f2 | tr -d ' ' || echo "")
        [ -n "$config_max_size" ] && MAX_INPUT_SIZE="$config_max_size"

        local config_timeout
        config_timeout=$(grep "stdin_timeout:" "$config_file" 2>/dev/null | cut -d':' -f2 | tr -d ' ' || echo "")
        [ -n "$config_timeout" ] && STDIN_TIMEOUT="$config_timeout"

        local config_debug
        config_debug=$(grep "debug_mode:" "$config_file" 2>/dev/null | cut -d':' -f2 | tr -d ' ' || echo "")
        [ "$config_debug" = "true" ] && DEBUG_MODE=true
    fi

    # Environment variable overrides
    [ -n "${BB5_MAX_INPUT_SIZE:-}" ] && MAX_INPUT_SIZE="$BB5_MAX_INPUT_SIZE"
    [ -n "${BB5_STDIN_TIMEOUT:-}" ] && STDIN_TIMEOUT="$BB5_STDIN_TIMEOUT"
    [ -n "${BB5_LOCK_TIMEOUT:-}" ] && LOCK_TIMEOUT="$BB5_LOCK_TIMEOUT"
    [ "${BB5_DEBUG:-}" = "true" ] && DEBUG_MODE=true

    # Validate values
    if ! [[ "$MAX_INPUT_SIZE" =~ ^[0-9]+$ ]]; then
        log_error "Invalid MAX_INPUT_SIZE: $MAX_INPUT_SIZE, using default"
        MAX_INPUT_SIZE=1048576
    fi
}
```

**Impact:** Medium
**Effort:** Medium
**Rationale:** Allows customization without code changes, supports different environments.

---

### 1.3 Metrics and Observability
**Problem:** No metrics collection or performance tracking. Cannot measure hook execution time or failure rates.

**Suggested Code:**
```bash
# At start of main()
main() {
    local start_time
    start_time=$(date +%s%N 2>/dev/null || echo "$(date +%s)000000000")

    # ... existing code ...

    # At end of main()
    local end_time
    end_time=$(date +%s%N 2>/dev/null || echo "$(date +%s)000000000")
    local duration_ms=$(( (end_time - start_time) / 1000000 ))

    # Log metrics
    log_metrics "$duration_ms" "${#ERRORS[@]}"
}

log_metrics() {
    local duration_ms="$1"
    local error_count="$2"

    local metrics_file="${BB5_METRICS_FILE:-$BB5_ROOT/.autonomous/metrics/hook-metrics.jsonl}"

    # Ensure directory exists
    mkdir -p "$(dirname "$metrics_file")" 2>/dev/null || return 0

    # Append metrics (JSON Lines format)
    cat >> "$metrics_file" << EOF
{"timestamp":"$(date -Iseconds)","hook":"SessionStart","duration_ms":$duration_ms,"errors":$error_count,"project":"${BB5_PROJECT:-unknown}","agent_type":"${BB5_AGENT_TYPE:-unknown}","mode":"${MODE:-unknown}"}
EOF
}
```

**Impact:** Medium
**Effort:** Easy
**Rationale:** Essential for monitoring hook performance in production.

---

### 1.4 Dry-Run Mode
**Problem:** No way to test the hook without side effects (creating run folders, modifying files).

**Suggested Code:**
```bash
# Add to configuration
DRY_RUN=false

# Check for dry-run mode
if [ "${BB5_DRY_RUN:-}" = "true" ] || [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=true
    log_info "DRY RUN MODE - No files will be modified"
fi

# Wrapper for file operations
dry_run_aware() {
    local operation="$1"
    shift

    if [ "$DRY_RUN" = "true" ]; then
        log_info "[DRY-RUN] Would execute: $operation $*"
        return 0
    else
        "$operation" "$@"
    fi
}

# Usage in create_run_folder()
if ! dry_run_aware mkdir -p "$run_dir" 2>/dev/null; then
    log_error "Failed to create run directory: $run_dir"
    # ...
fi
```

**Impact:** Low
**Effort:** Medium
**Rationale:** Useful for testing and CI/CD pipelines.

---

## 2. CODE SMELLS

### 2.1 Inconsistent Error Handling Pattern
**Problem:** Some functions return error codes that are checked, others use `|| true` inconsistently.

**Current State:**
```bash
# Line 330-331: flock error suppressed
if flock -w "$timeout" -x "$lock_fd" 2>/dev/null; then

# Line 710: awk error suppressed
' "$env_file" > "$temp_file" 2>/dev/null || true
```

**Suggested Code:**
```bash
# Consistent error handling strategy
# Option 1: Always log errors, never suppress silently
if ! flock -w "$timeout" -x "$lock_fd" 2>/dev/null; then
    log_error "Failed to acquire lock on $lock_file (timeout: ${timeout}s)"
    return 1
fi

# Option 2: Explicitly document when errors are expected/acceptable
# Suppress expected errors (file doesn't exist yet)
if [ -f "$env_file" ]; then
    if ! awk -v start="$section_start" -v end="$section_end" '
        $0 == start { skip=1; next }
        $0 == end { skip=0; next }
        !skip { print }
    ' "$env_file" > "$temp_file" 2>/dev/null; then
        log_debug "awk processing had issues, continuing with empty content"
        : > "$temp_file"  # Create empty file
    fi
fi
```

**Impact:** High
**Effort:** Easy
**Rationale:** Silent failures make debugging difficult.

---

### 2.2 Repetitive Code in detect_agent_type()
**Problem:** Same pattern repeated for each agent type detection method.

**Current State:**
```bash
# Lines 498-527: Nearly identical blocks for each agent type
if [[ "$cwd" == *"/planner/"* ]] || [[ "$cwd" == *".autonomous/agents/planner"* ]]; then
    detected_type="planner"
    confidence=90
    log_debug "Agent type detected from cwd path: $detected_type"
    echo "$detected_type"
    return 0
elif [[ "$cwd" == *"/executor/"* ]] || [[ "$cwd" == *".autonomous/agents/executor"* ]]; then
    # ... identical pattern
```

**Suggested Code:**
```bash
# Refactored with lookup table
detect_agent_type_from_path() {
    local path="$1"
    local agent_types="planner:planner executor:executor architect:architect scout:scout verifier:verifier"

    for pair in $agent_types; do
        local type="${pair%%:*}"
        if [[ "$path" == *"/${type}/"* ]] || [[ "$path" == *".autonomous/agents/${type}"* ]]; then
            echo "$type"
            return 0
        fi
    done
    return 1
}

# Or using a more maintainable pattern
AGENT_PATH_PATTERNS=(
    "planner:/planner/:.autonomous/agents/planner"
    "executor:/executor/:.autonomous/agents/executor"
    "architect:/architect/:.autonomous/agents/architect"
    "scout:/scout/:.autonomous/agents/scout"
    "verifier:/verifier/:.autonomous/agents/verifier"
)

detect_agent_type() {
    local cwd="$(pwd)"

    for pattern in "${AGENT_PATH_PATTERNS[@]}"; do
        IFS=':' read -r agent_type path_pattern dir_pattern <<< "$pattern"
        if [[ "$cwd" == *"$path_pattern"* ]] || [[ "$cwd" == *"$dir_pattern"* ]]; then
            log_debug "Agent type detected from cwd path: $agent_type"
            echo "$agent_type"
            return 0
        fi
    done

    # ... rest of detection logic
}
```

**Impact:** Medium
**Effort:** Easy
**Rationale:** Reduces code duplication, easier to add new agent types.

---

### 2.3 Magic Numbers and Strings
**Problem:** Hardcoded values scattered throughout the code.

**Current State:**
```bash
confidence=100  # What does 100 mean?
confidence=95   # vs 95?
confidence=90   # vs 90?
# No documentation of confidence thresholds
```

**Suggested Code:**
```bash
# Define confidence levels as constants
readonly CONFIDENCE_OVERRIDE=100      # Environment variable override
readonly CONFIDENCE_EXPLICIT_FILE=95  # Explicit .bb5-project file
readonly CONFIDENCE_PATH_PATTERN=90   # Path-based detection
readonly CONFIDENCE_FILE_HEURISTIC=85 # File-based heuristic
readonly CONFIDENCE_GIT_BRANCH=80     # Git branch pattern
readonly CONFIDENCE_DEFAULT=50        # Default fallback

# Usage
if [ -n "${BB5_PROJECT:-}" ]; then
    detected_project="$BB5_PROJECT"
    confidence=$CONFIDENCE_OVERRIDE
    # ...
fi
```

**Impact:** Low
**Effort:** Easy
**Rationale:** Self-documenting code, easier maintenance.

---

## 3. OPTIMIZATION OPPORTUNITIES

### 3.1 Reduce Subshell Usage
**Problem:** Multiple `$(...)` calls can be expensive, especially in tight loops or repeated operations.

**Current State:**
```bash
# Line 381: Subshell for pwd
detect_project() {
    local cwd="$(pwd)"  # Subshell 1
    # ...
    dir=$(dirname "$dir")  # Subshell 2 (in loop!)
}

# Line 750-752: Multiple git calls
git_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
git_commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
```

**Suggested Code:**
```bash
# Cache expensive operations
detect_project() {
    local cwd
    cwd="$PWD"  # Use builtin instead of $(pwd)
    # ...
}

# Batch git operations
get_git_info() {
    local git_info
    if git_info=$(git rev-parse --abbrev-ref HEAD --short HEAD 2>/dev/null); then
        echo "$git_info" | tr '\n' '|'
    else
        echo "unknown|unknown"
    fi
}

# Usage
git_info=$(get_git_info)
git_branch="${git_info%%|*}"
git_commit="${git_info##*|}"
```

**Impact:** Medium
**Effort:** Easy
**Rationale:** Reduces fork/exec overhead, faster execution.

---

### 3.2 Lazy Evaluation for Template Files
**Problem:** All 6 template files are created even if they won't be used.

**Current State:**
```bash
# Lines 854-1087: Always creates all template files
create_template_files() {
    # Creates THOUGHTS.md, RESULTS.md, DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md, metadata.yaml
    # All 6 files every time
}
```

**Suggested Code:**
```bash
# Only create files when needed
create_template_files() {
    local run_dir="$1"
    local project="$2"
    local agent_type="$3"

    # Always create minimal set
    create_thoughts_template "$run_dir" "$project" "$agent_type"
    create_metadata_template "$run_dir" "$project" "$agent_type"

    # Conditionally create based on mode
    if [ "$mode" = "autonomous" ]; then
        create_results_template "$run_dir" "$project" "$agent_type"
    fi

    # Create others on-demand or based on configuration
    if [ "${BB5_FULL_TEMPLATES:-}" = "true" ]; then
        create_decisions_template "$run_dir" "$project" "$agent_type"
        create_assumptions_template "$run_dir" "$project" "$agent_type"
        create_learnings_template "$run_dir" "$project" "$agent_type"
    fi
}
```

**Impact:** Medium
**Effort:** Easy
**Rationale:** Faster execution, less disk I/O for simple sessions.

---

### 3.3 Parallelize Independent Operations
**Problem:** Sequential execution of independent detection operations.

**Current State:**
```bash
main() {
    # Sequential execution
    project=$(detect_project)      # Wait
    agent_type=$(detect_agent_type) # Wait
    mode=$(detect_mode)             # Wait
}
```

**Suggested Code:**
```bash
# Note: This is bash-specific, not POSIX
# For POSIX, sequential is fine - detection is fast enough

# Alternative: Background file operations
main() {
    # Detection is fast, keep sequential
    project=$(detect_project)
    agent_type=$(detect_agent_type)
    mode=$(detect_mode)

    # Create run folder
    create_run_folder "$project" "$agent_type"

    # Parallelize independent file operations (if using bash)
    {
        persist_environment_vars "$CLAUDE_ENV_FILE" "$project" "$agent_type" "$RUN_DIR" "$RUN_ID"
    } &

    {
        create_template_files "$RUN_DIR" "$project" "$agent_type"
    } &

    {
        generate_agent_context "$RUN_DIR" "$project" "$agent_type" "$mode"
    } &

    # Wait for all background jobs
    wait
}
```

**Impact:** Low
**Effort:** Medium
**Rationale:** Marginal gains for this use case; sequential is simpler and fast enough.

---

## 4. SAFETY ISSUES

### 4.1 Path Traversal Vulnerability
**Problem:** User-controlled input (project name from file) used in path construction without validation.

**Current State:**
```bash
# Line 397-399: Project name from file used directly
project_from_file=$(cat ".bb5-project" 2>/dev/null | tr -d '[:space:]')
if [ -n "$project_from_file" ]; then
    detected_project="$project_from_file"
    # Later used in: mkdir -p "$BB5_ROOT/5-project-memory/$project/..."
```

**Suggested Code:**
```bash
validate_project_name() {
    local name="$1"

    # Reject names with path traversal
    if [[ "$name" == *".."* ]] || [[ "$name" == *"/"* ]] || [[ "$name" == *"\\"* ]]; then
        log_error "Invalid project name (path traversal attempt): $name"
        return 1
    fi

    # Reject names starting with dot (hidden)
    if [[ "$name" == .* ]]; then
        log_error "Invalid project name (hidden file): $name"
        return 1
    fi

    # Reject empty or whitespace-only
    if [[ -z "${name// /}" ]]; then
        log_error "Invalid project name (empty)"
        return 1
    fi

    # Allow only alphanumeric, hyphen, underscore
    if [[ ! "$name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        log_error "Invalid project name (invalid characters): $name"
        return 1
    fi

    return 0
}

# Usage
project_from_file=$(cat ".bb5-project" 2>/dev/null | tr -d '[:space:]')
if [ -n "$project_from_file" ] && validate_project_name "$project_from_file"; then
    detected_project="$project_from_file"
fi
```

**Impact:** Critical
**Effort:** Easy
**Rationale:** Prevents directory traversal attacks.

---

### 4.2 Race Condition in mktemp
**Problem:** `mktemp` followed by append (`>>`) is not atomic.

**Current State:**
```bash
# Line 698-724: mktemp then append
temp_file=$(mktemp "${env_file}.tmp.XXXXXX")
# ... copy content ...
{
    echo "$section_start"
    # ...
} >> "$temp_file"  # Append, not atomic
mv "$temp_file" "$env_file"
```

**Suggested Code:**
```bash
# Use atomic write pattern
persist_environment_vars() {
    local env_file="$1"
    # ...

    # Create temp file in same directory for atomic move
    local temp_file
    temp_file=$(mktemp -p "$(dirname "$env_file")" "$(basename "$env_file").tmp.XXXXXX")

    # Ensure cleanup on exit
    trap 'rm -f "$temp_file"' EXIT

    # Write all content at once (single write)
    {
        if [ -f "$env_file" ]; then
            awk -v start="$section_start" -v end="$section_end" '
                $0 == start { skip=1; next }
                $0 == end { skip=0; next }
                !skip { print }
            ' "$env_file" 2>/dev/null
        fi

        echo ""
        echo "$section_start"
        echo "# Generated: $(date -Iseconds)"
        echo "export BB5_PROJECT='$(escape_for_shell "$project")'"
        # ...
        echo "$section_end"
    } > "$temp_file"  # Single redirect, not append

    # Atomic move
    if mv "$temp_file" "$env_file"; then
        trap - EXIT  # Clear trap on success
        return 0
    else
        rm -f "$temp_file"
        return 1
    fi
}
```

**Impact:** High
**Effort:** Easy
**Rationale:** Prevents partial file writes on crash.

---

### 4.3 Signal Handling
**Problem:** No trap for cleanup on interruption.

**Suggested Code:**
```bash
# Global temp file tracking
TEMP_FILES=()

cleanup() {
    local exit_code=$?

    # Remove all temp files
    for temp_file in "${TEMP_FILES[@]}"; do
        [ -f "$temp_file" ] && rm -f "$temp_file"
    done

    # Release any held locks
    if [ -n "${LOCK_FD:-}" ]; then
        flock -u "$LOCK_FD" 2>/dev/null || true
        exec {LOCK_FD}>&- 2>/dev/null || true
    fi

    exit $exit_code
}

trap cleanup EXIT INT TERM

# When creating temp files
register_temp_file() {
    TEMP_FILES+=("$1")
}
```

**Impact:** Medium
**Effort:** Easy
**Rationale:** Prevents temp file accumulation on interruption.

---

### 4.4 Insufficient Input Validation
**Problem:** JSON input size limit is checked but not enforced properly; no validation of JSON structure.

**Current State:**
```bash
# Line 362: Only reads up to limit, but doesn't validate total size
if IFS= read -r -t "$STDIN_TIMEOUT" -n "$MAX_INPUT_SIZE" input 2>/dev/null; then
```

**Suggested Code:**
```bash
read_stdin_input() {
    local input=""
    local total_read=0
    local chunk

    # Check if stdin is a terminal
    if [ -t 0 ]; then
        echo "{}"
        return 0
    fi

    # Read in chunks to enforce limit strictly
    while IFS= read -r -t "$STDIN_TIMEOUT" -n 4096 chunk 2>/dev/null; do
        total_read=$((total_read + ${#chunk}))

        if [ $total_read -gt "$MAX_INPUT_SIZE" ]; then
            log_error "Input exceeds maximum size ($MAX_INPUT_SIZE bytes)"
            echo "{}"
            return 1
        fi

        input="${input}${chunk}"

        # Check if we have complete JSON (ends with })
        [[ "$chunk" == *} ]] && break
    done

    # Validate JSON structure
    if [ -n "$input" ] && echo "$input" | jq -e . >/dev/null 2>&1; then
        # Validate expected schema
        if echo "$input" | jq -e 'has("source") or has("session_id")' >/dev/null 2>&1; then
            echo "$input"
        else
            log_debug "JSON missing expected fields, using empty object"
            echo "{}"
        fi
    else
        echo "{}"
    fi
}
```

**Impact:** High
**Effort:** Medium
**Rationale:** Better protection against malformed input.

---

## 5. STANDARDS COMPLIANCE

### 5.1 POSIX Compliance Issues
**Problem:** Uses several bashisms that reduce portability.

**Current State:**
```bash
#!/bin/bash  # Bash-specific

# Line 329: Brace expansion (bash-specific)
exec {lock_fd}>"$lock_file"

# Line 425: [[ ]] test (bash-specific)
if [[ "$cwd" == *"5-project-memory/blackbox5"* ]]; then

# Line 233: Array usage (bash-specific)
ERRORS+=("$message")

# Line 1191: Array length (bash-specific)
if [ ${#ERRORS[@]} -gt 0 ]; then
```

**Suggested Code:**
```bash
#!/bin/sh  # POSIX-compliant

# For flock, use a different approach (flock is not POSIX either)
# Option 1: Use mkdir for atomic lock (POSIX)
acquire_lock() {
    local lock_file="$1"
    local timeout="${2:-$LOCK_TIMEOUT}"
    local waited=0

    while [ $waited -lt "$timeout" ]; do
        if mkdir "$lock_file" 2>/dev/null; then
            # Lock acquired
            echo "$lock_file"
            return 0
        fi
        sleep 1
        waited=$((waited + 1))
    done

    return 1
}

release_lock() {
    local lock_file="$1"
    rmdir "$lock_file" 2>/dev/null || true
}

# Use [ ] instead of [[ ]]
if [ "${cwd#*5-project-memory/blackbox5}" != "$cwd" ]; then
    # Pattern matched
fi

# Use string accumulation instead of arrays
ERRORS=""
log_error() {
    local message="$1"
    ERRORS="${ERRORS}${ERRORS:+, }$message"
    echo "[ERROR] $message" >&2
}

# Check for errors
if [ -n "$ERRORS" ]; then
    # Has errors
fi
```

**Impact:** Medium
**Effort:** Hard
**Rationale:** POSIX compliance ensures portability across different systems.

**Recommendation:** Given this is specifically for Claude Code on macOS/Linux with bash available, keeping bash is acceptable. However, document this assumption:

```bash
#!/bin/bash
# NOTE: This script requires bash (not POSIX sh) for:
# - Arrays (ERRORS tracking)
# - [[ ]] pattern matching
# - Brace expansion (file descriptors)
# Claude Code runs on macOS/Linux with bash 3.2+ available
```

---

### 5.2 ShellCheck Compliance
**Problem:** Several ShellCheck warnings likely present (can't verify without shellcheck installed).

**Likely Issues:**
```bash
# SC2086: Double quote to prevent globbing and word splitting
# Current:
echo $input | jq -e .
# Fixed:
echo "$input" | jq -e .

# SC2181: Check exit code directly
# Current:
if [ $? -eq 0 ]; then
# Fixed:
if echo "$input" | jq -e .; then

# SC2006: Use $(..) instead of legacy `..`
# Current:
project=`cat .bb5-project`
# Fixed:
project=$(cat .bb5-project)
```

**Suggested Code:**
```bash
# Add shellcheck directive comments for intentional exceptions
# shellcheck disable=SC2039  # We require bash for arrays
ERRORS=()

# Or fix the issues:
# Always quote variables
echo "$input" | jq -e . >/dev/null 2>&1

# Check exit codes directly
if command -v jq >/dev/null 2>&1; then
    # jq exists
fi
```

**Impact:** Low
**Effort:** Easy
**Rationale:** Static analysis catches common bugs.

---

### 5.3 Documentation Standards
**Problem:** Function documentation is inconsistent; no standardized docstring format.

**Current State:**
```bash
# Some functions have comments, others don't
acquire_lock() {
    local lock_file="$1"
    # ...
}

# No documentation for parameters, return values, or side effects
```

**Suggested Code:**
```bash
# Standardized documentation format
#######################################
# Acquire an exclusive lock on a file.
# Arguments:
#   $1 - Path to lock file
#   $2 - Timeout in seconds (optional, default: $LOCK_TIMEOUT)
# Returns:
#   0 on success, 1 on timeout
# Outputs:
#   Echoes lock file descriptor number on success
# Side Effects:
#   Creates lock file if it doesn't exist
#######################################
acquire_lock() {
    local lock_file="$1"
    local timeout="${2:-$LOCK_TIMEOUT}"
    # ...
}

# Or use a simpler format:
# acquire_lock(lock_file, [timeout]) -> lock_fd or failure
# Acquire exclusive lock with timeout
```

**Impact:** Low
**Effort:** Easy
**Rationale:** Consistent documentation aids maintenance.

---

## Summary Table

| # | Issue | Category | Impact | Effort | Priority |
|---|-------|----------|--------|--------|----------|
| 1 | Dependency Validation | Missing Feature | Critical | Easy | P0 |
| 2 | Path Traversal Protection | Safety | Critical | Easy | P0 |
| 3 | Race Condition in mktemp | Safety | High | Easy | P0 |
| 4 | Inconsistent Error Handling | Code Smell | High | Easy | P1 |
| 5 | Input Validation | Safety | High | Medium | P1 |
| 6 | Signal Handling | Safety | Medium | Easy | P1 |
| 7 | Configuration File Support | Missing Feature | Medium | Medium | P2 |
| 8 | Metrics Collection | Missing Feature | Medium | Easy | P2 |
| 9 | Code Duplication in detect_agent_type | Code Smell | Medium | Easy | P2 |
| 10 | Reduce Subshell Usage | Optimization | Medium | Easy | P2 |
| 11 | Lazy Template Creation | Optimization | Medium | Easy | P2 |
| 12 | POSIX Compliance | Standards | Medium | Hard | P3 |
| 13 | ShellCheck Compliance | Standards | Low | Easy | P3 |
| 14 | Magic Numbers | Code Smell | Low | Easy | P3 |
| 15 | Documentation Standards | Standards | Low | Easy | P3 |
| 16 | Dry-Run Mode | Missing Feature | Low | Medium | P4 |
| 17 | Parallel Operations | Optimization | Low | Medium | P4 |

---

## Recommended Implementation Order

### Phase 1: Critical Safety (P0)
1. Add dependency validation
2. Add path traversal protection
3. Fix race condition in mktemp
4. Standardize error handling

### Phase 2: Reliability (P1)
5. Enhance input validation
6. Add signal handling with cleanup

### Phase 3: Maintainability (P2)
7. Add configuration file support
8. Add metrics collection
9. Refactor detect_agent_type to reduce duplication
10. Optimize subshell usage
11. Implement lazy template creation

### Phase 4: Polish (P3-P4)
12. Document bash dependency (or make POSIX-compliant)
13. Run ShellCheck and fix warnings
14. Replace magic numbers with constants
15. Standardize documentation format
16. Add dry-run mode (optional)

---

## Sources

- [Claude Code Hooks Guide](https://hexdocs.pm/claude_agent_sdk/hooks_guide.html)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck Documentation](https://www.shellcheck.net/)
- [POSIX Shell Specification](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [Shell Scripting Best Practices](https://sharats.me/posts/shell-script-best-practices/)

---

*Analysis completed by DevOps Engineer Agent*
*Quality improvement potential: 92/100 → 98/100*
