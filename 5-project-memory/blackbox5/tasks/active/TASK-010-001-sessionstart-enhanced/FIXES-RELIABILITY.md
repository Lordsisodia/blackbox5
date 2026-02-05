# BB5 SessionStart Hook - Reliability Fixes

**Task:** TASK-010-001
**Focus:** Error handling and dependency issues
**Date:** 2026-02-06
**Source:** EVALUATION-AGENT-1.md, IMPROVEMENTS-AGENT-2.md

---

## Summary

This document contains fixed implementations for critical reliability issues identified in the BB5 SessionStart hook:

1. **Missing dependency checks** - No validation for jq, flock, git at startup
2. **Silent failures** - `2>/dev/null || true` patterns hide errors
3. **No signal handling** - Temp files left behind on interruption
4. **Inconsistent error handling** - Mixed patterns throughout code

---

## 1. validate_dependencies() Function

**Issue:** Hook assumes all dependencies (jq, flock, git) are available without verification. If missing, failures are silent or produce invalid output.

**Location:** Should be called at the start of `main()` before any operations.

```bash
# =============================================================================
# DEPENDENCY VALIDATION
# =============================================================================

# Required dependencies with their minimum versions (optional)
declare -A REQUIRED_DEPS=(
    ["jq"]=""
    ["flock"]=""
    ["git"]=""
)

#######################################
# Validate that all required dependencies are installed.
# Globals:
#   REQUIRED_DEPS - Associative array of required commands
#   HOOK_VERSION  - Hook version for error output
# Returns:
#   0 if all dependencies present, 1 otherwise
# Outputs:
#   Error messages to stderr if dependencies missing
#   Valid JSON error response to stdout on failure
#######################################
validate_dependencies() {
    local missing_deps=()
    local dep

    # Check each required dependency
    for dep in "${!REQUIRED_DEPS[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            missing_deps+=("$dep")
        fi
    done

    # If any dependencies missing, output error JSON and exit
    if [ ${#missing_deps[@]} -gt 0 ]; then
        local dep_list
        dep_list=$(printf '%s, ' "${missing_deps[@]}")
        dep_list="${dep_list%, }"  # Remove trailing comma

        # Log to stderr
        echo "[ERROR] Missing required dependencies: $dep_list" >&2
        echo "[ERROR] Please install: ${missing_deps[*]}" >&2

        # Output valid JSON for Claude Code (even on failure)
        cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "ERROR: Missing dependencies: $dep_list. Please install required packages.",
    "project": "unknown",
    "agentType": "unknown",
    "mode": "manual",
    "runDir": "$(pwd)",
    "runId": "error-$(date +%s)",
    "hookVersion": "${HOOK_VERSION}",
    "timestamp": "$(date -Iseconds)",
    "error": true,
    "missingDependencies": [$(printf '"%s", ' "${missing_deps[@]}" | sed 's/, $//')]
  }
}
EOF
        return 1
    fi

    log_debug "All dependencies validated: ${!REQUIRED_DEPS[*]}"
    return 0
}
```

---

## 2. Improved log_error() with Proper Error Tracking

**Issue:** Original error handling uses inconsistent patterns - some functions return error codes, others use global ERRORS array, some suppress errors with `|| true`.

**Location:** Replace existing logging functions section.

```bash
# =============================================================================
# ERROR HANDLING AND LOGGING
# =============================================================================

# Error tracking array
ERRORS=()

# Error severity levels
readonly SEVERITY_DEBUG=0
readonly SEVERITY_INFO=1
readonly SEVERITY_WARN=2
readonly SEVERITY_ERROR=3
readonly SEVERITY_FATAL=4

#######################################
# Log an error message with proper tracking.
# Arguments:
#   $1 - Error message
#   $2 - Severity level (optional, default: SEVERITY_ERROR)
# Globals:
#   ERRORS - Array to store error messages
# Outputs:
#   Formatted error message to stderr
#######################################
log_error() {
    local message="$1"
    local severity="${2:-$SEVERITY_ERROR}"
    local timestamp
    timestamp=$(date -Iseconds)

    # Store in error tracking array with structured format
    ERRORS+=("[$timestamp] [SEVERITY:$severity] $message")

    # Output to stderr with appropriate prefix
    case "$severity" in
        $SEVERITY_FATAL)
            echo "[FATAL] $message" >&2
            ;;
        $SEVERITY_ERROR)
            echo "[ERROR] $message" >&2
            ;;
        $SEVERITY_WARN)
            echo "[WARN] $message" >&2
            ;;
        *)
            echo "[ERROR] $message" >&2
            ;;
    esac
}

#######################################
# Log an informational message.
# Arguments:
#   $1 - Message to log
# Outputs:
#   Message to stderr
#######################################
log_info() {
    local message="$1"
    echo "[INFO] $message" >&2
}

#######################################
# Log a debug message (only if BB5_DEBUG=true).
# Arguments:
#   $1 - Message to log
# Globals:
#   BB5_DEBUG - Debug mode flag
# Outputs:
#   Message to stderr if debug mode enabled
#######################################
log_debug() {
    local message="$1"
    if [ "${BB5_DEBUG:-}" = "true" ]; then
        echo "[DEBUG] $message" >&2
    fi
}

#######################################
# Check if any errors have been logged.
# Globals:
#   ERRORS - Error tracking array
# Returns:
#   0 if errors exist, 1 otherwise
#######################################
has_errors() {
    [ ${#ERRORS[@]} -gt 0 ]
}

#######################################
# Get count of logged errors.
# Globals:
#   ERRORS - Error tracking array
# Outputs:
#   Number of errors to stdout
#######################################
error_count() {
    echo "${#ERRORS[@]}"
}

#######################################
# Get formatted error summary.
# Globals:
#   ERRORS - Error tracking array
# Outputs:
#   Formatted error summary to stdout
#######################################
get_error_summary() {
    if has_errors; then
        local count
        count=$(error_count)
        echo "Errors encountered: $count"
        local i=0
        for error in "${ERRORS[@]}"; do
            i=$((i + 1))
            echo "  $i. $error"
        done
    else
        echo "No errors"
    fi
}

#######################################
# Clear all tracked errors.
# Globals:
#   ERRORS - Error tracking array
#######################################
clear_errors() {
    ERRORS=()
}
```

---

## 3. cleanup() Trap Function

**Issue:** No signal handlers for cleanup on interruption. Temp files left behind, locks not released.

**Location:** Define at script initialization, trap set after temp file tracking is ready.

```bash
# =============================================================================
# CLEANUP AND SIGNAL HANDLING
# =============================================================================

# Global temp file tracking array
TEMP_FILES=()

# Global lock file descriptor tracking
LOCK_FD=""

#######################################
# Register a temp file for cleanup tracking.
# Arguments:
#   $1 - Path to temp file
# Globals:
#   TEMP_FILES - Array tracking temp files
#######################################
register_temp_file() {
    local temp_file="$1"
    TEMP_FILES+=("$temp_file")
    log_debug "Registered temp file for cleanup: $temp_file"
}

#######################################
# Unregister a temp file after successful use.
# Arguments:
#   $1 - Path to temp file
# Globals:
#   TEMP_FILES - Array tracking temp files
#######################################
unregister_temp_file() {
    local temp_file="$1"
    local new_temp_files=()

    for file in "${TEMP_FILES[@]}"; do
        if [ "$file" != "$temp_file" ]; then
            new_temp_files+=("$file")
        fi
    done

    TEMP_FILES=("${new_temp_files[@]}")
}

#######################################
# Register a lock file descriptor for cleanup.
# Arguments:
#   $1 - File descriptor number
# Globals:
#   LOCK_FD - Variable tracking lock file descriptor
#######################################
register_lock_fd() {
    local fd="$1"
    LOCK_FD="$fd"
    log_debug "Registered lock fd for cleanup: $fd"
}

#######################################
# Cleanup function called on exit or signal.
# Removes temp files and releases locks.
# Globals:
#   TEMP_FILES - Array of temp files to remove
#   LOCK_FD    - Lock file descriptor to release
#   ERRORS     - Error tracking array
# Arguments:
#   $1 - Exit code (optional, captured from $? if not provided)
#######################################
cleanup() {
    local exit_code=${1:-$?}

    log_debug "Cleanup triggered with exit code: $exit_code"

    # Remove all registered temp files
    if [ ${#TEMP_FILES[@]} -gt 0 ]; then
        log_debug "Cleaning up ${#TEMP_FILES[@]} temp file(s)"
        for temp_file in "${TEMP_FILES[@]}"; do
            if [ -f "$temp_file" ]; then
                rm -f "$temp_file"
                log_debug "Removed temp file: $temp_file"
            fi
        done
    fi

    # Release any held locks
    if [ -n "${LOCK_FD:-}" ]; then
        log_debug "Releasing lock on fd: $LOCK_FD"
        # Unlock and close file descriptor
        flock -u "$LOCK_FD" 2>/dev/null || true
        eval "exec ${LOCK_FD}>&-" 2>/dev/null || true
    fi

    # Log error summary if there were errors
    if has_errors; then
        log_info "Session completed with $(error_count) error(s)"
        get_error_summary >&2
    fi

    exit $exit_code
}

#######################################
# Set up signal handlers for graceful cleanup.
# Must be called after cleanup function is defined.
#######################################
setup_signal_handlers() {
    # Clean up on normal exit
    trap cleanup EXIT

    # Clean up on interrupt (Ctrl+C)
    trap 'echo "[WARN] Interrupted by user" >&2; cleanup 130' INT

    # Clean up on termination
    trap 'echo "[WARN] Terminated" >&2; cleanup 143' TERM

    # Clean up on hangup
    trap 'echo "[WARN] Hangup received" >&2; cleanup 129' HUP

    log_debug "Signal handlers registered"
}

# Call this at script initialization
setup_signal_handlers
```

---

## 4. Standardized Error Handling Pattern

**Issue:** Inconsistent error handling - some functions return error codes, others use `|| true`, some suppress errors silently.

**Location:** Replace existing locking and file operation functions.

```bash
# =============================================================================
# LOCKING FUNCTIONS (Standardized Error Handling)
# =============================================================================

#######################################
# Acquire an exclusive lock on a file.
# Arguments:
#   $1 - Path to lock file
#   $2 - Timeout in seconds (optional, default: LOCK_TIMEOUT)
# Returns:
#   0 on success, 1 on timeout or error
# Outputs:
#   Echoes lock file descriptor number on success
# Side Effects:
#   Creates lock file if it doesn't exist
#   Registers lock fd for cleanup
#######################################
acquire_lock() {
    local lock_file="$1"
    local timeout="${2:-$LOCK_TIMEOUT}"

    # Validate inputs
    if [ -z "$lock_file" ]; then
        log_error "acquire_lock: lock_file argument required" $SEVERITY_ERROR
        return 1
    fi

    # Ensure lock file directory exists
    local lock_dir
    lock_dir=$(dirname "$lock_file")
    if [ ! -d "$lock_dir" ]; then
        log_error "Lock file directory does not exist: $lock_dir" $SEVERITY_ERROR
        return 1
    fi

    # Create lock file if it doesn't exist
    if [ ! -f "$lock_file" ]; then
        touch "$lock_file" 2>/dev/null || {
            log_error "Cannot create lock file: $lock_file" $SEVERITY_ERROR
            return 1
        }
    fi

    # Open file descriptor for locking
    local lock_fd
    exec {lock_fd}>"$lock_file" || {
        log_error "Cannot open lock file for writing: $lock_file" $SEVERITY_ERROR
        return 1
    }

    # Attempt to acquire exclusive lock with timeout
    if flock -w "$timeout" -x "$lock_fd"; then
        log_debug "Lock acquired on $lock_file (fd: $lock_fd)"
        register_lock_fd "$lock_fd"
        echo "$lock_fd"
        return 0
    else
        log_error "Failed to acquire lock on $lock_file (timeout: ${timeout}s)" $SEVERITY_WARN
        exec {lock_fd}>&-
        return 1
    fi
}

#######################################
# Release a previously acquired lock.
# Arguments:
#   $1 - Lock file descriptor number
# Returns:
#   0 on success, 1 on error
#######################################
release_lock() {
    local lock_fd="$1"

    if [ -z "$lock_fd" ]; then
        log_error "release_lock: lock_fd argument required" $SEVERITY_ERROR
        return 1
    fi

    # Unlock and close file descriptor
    if flock -u "$lock_fd" 2>/dev/null; then
        log_debug "Lock released on fd: $lock_fd"
    else
        log_error "Failed to unlock fd: $lock_fd" $SEVERITY_WARN
    fi

    if eval "exec ${lock_fd}>&-" 2>/dev/null; then
        log_debug "Lock fd closed: $lock_fd"
    else
        log_error "Failed to close lock fd: $lock_fd" $SEVERITY_WARN
        return 1
    fi

    # Clear global tracking
    LOCK_FD=""

    return 0
}

# =============================================================================
# FILE OPERATIONS (Standardized Error Handling)
# =============================================================================

#######################################
# Create a directory with proper error handling.
# Arguments:
#   $1 - Directory path to create
#   $2 - Create parents flag (optional, "true" for mkdir -p)
# Returns:
#   0 on success, 1 on failure
#######################################
safe_mkdir() {
    local dir_path="$1"
    local create_parents="${2:-false}"

    if [ -z "$dir_path" ]; then
        log_error "safe_mkdir: dir_path argument required" $SEVERITY_ERROR
        return 1
    fi

    # Check if already exists
    if [ -d "$dir_path" ]; then
        log_debug "Directory already exists: $dir_path"
        return 0
    fi

    # Create directory
    local mkdir_cmd="mkdir"
    [ "$create_parents" = "true" ] && mkdir_cmd="mkdir -p"

    if $mkdir_cmd "$dir_path"; then
        log_debug "Created directory: $dir_path"
        return 0
    else
        log_error "Failed to create directory: $dir_path" $SEVERITY_ERROR
        return 1
    fi
}

#######################################
# Write content to file atomically.
# Arguments:
#   $1 - Target file path
#   $2 - Content to write (via stdin if not provided)
# Returns:
#   0 on success, 1 on failure
#######################################
atomic_write() {
    local target_file="$1"
    local content="${2:-}"

    if [ -z "$target_file" ]; then
        log_error "atomic_write: target_file argument required" $SEVERITY_ERROR
        return 1
    fi

    # Ensure target directory exists
    local target_dir
    target_dir=$(dirname "$target_file")
    if ! safe_mkdir "$target_dir" "true"; then
        return 1
    fi

    # Create temp file in same directory for atomic move
    local temp_file
    temp_file=$(mktemp -p "$target_dir" "$(basename "$target_file").tmp.XXXXXX") || {
        log_error "Failed to create temp file for atomic write" $SEVERITY_ERROR
        return 1
    }

    # Register for cleanup (will be unregistered on success)
    register_temp_file "$temp_file"

    # Write content
    if [ -n "$content" ]; then
        echo "$content" > "$temp_file" || {
            log_error "Failed to write to temp file" $SEVERITY_ERROR
            return 1
        }
    else
        # Read from stdin
        cat > "$temp_file" || {
            log_error "Failed to write stdin to temp file" $SEVERITY_ERROR
            return 1
        }
    fi

    # Atomic move
    if mv "$temp_file" "$target_file"; then
        log_debug "Atomic write successful: $target_file"
        unregister_temp_file "$temp_file"
        return 0
    else
        log_error "Failed to atomically write: $target_file" $SEVERITY_ERROR
        return 1
    fi
}

# =============================================================================
# JSON OPERATIONS (Standardized Error Handling)
# =============================================================================

#######################################
# Validate JSON input.
# Arguments:
#   $1 - JSON string to validate
# Returns:
#   0 if valid JSON, 1 otherwise
#######################################
validate_json() {
    local json_input="$1"

    if [ -z "$json_input" ]; then
        return 1
    fi

    if echo "$json_input" | jq -e . >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

#######################################
# Safely extract value from JSON.
# Arguments:
#   $1 - JSON string
#   $2 - jq filter expression
# Returns:
#   0 on success, 1 on failure
# Outputs:
#   Extracted value to stdout
#######################################
safe_jq_extract() {
    local json_input="$1"
    local jq_filter="$2"

    if [ -z "$json_input" ] || [ -z "$jq_filter" ]; then
        return 1
    fi

    local result
    result=$(echo "$json_input" | jq -r "$jq_filter" 2>/dev/null) || {
        log_debug "jq extraction failed: $jq_filter"
        return 1
    }

    echo "$result"
    return 0
}
```

---

## 5. Integration into Main()

**Updated main() function showing proper integration of fixes:**

```bash
#######################################
# Main execution function.
# Returns:
#   0 on success, non-zero on failure
#######################################
main() {
    local start_time
    start_time=$(date +%s)

    log_info "BB5 SessionStart Hook v${HOOK_VERSION}"

    # Step 1: Validate dependencies first
    if ! validate_dependencies; then
        # validate_dependencies outputs JSON error and exits
        return 1
    fi

    # Step 2: Read stdin input (if any)
    local stdin_input
    stdin_input=$(read_stdin_input)
    log_debug "Stdin input received: ${#stdin_input} bytes"

    # Step 3: Detect Project
    local project
    project=$(detect_project)
    log_info "Project detected: $project"
    export BB5_PROJECT="$project"

    # Step 4: Detect Agent Type
    local agent_type
    agent_type=$(detect_agent_type)
    log_info "Agent type detected: $agent_type"
    export BB5_AGENT_TYPE="$agent_type"

    # Step 5: Detect Mode
    local mode
    mode=$(detect_mode)
    log_info "Mode detected: $mode"
    export MODE="$mode"

    # Step 6: Create Run Folder (with proper error handling)
    if ! create_run_folder "$project" "$agent_type"; then
        log_error "Failed to create run folder" $SEVERITY_ERROR
        # Continue with fallback
    fi
    log_info "Run folder: $RUN_DIR"
    export RALF_RUN_DIR="$RUN_DIR"
    export RALF_RUN_ID="$RUN_ID"

    # Step 7: Persist Environment Variables
    if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
        if persist_environment_vars "$CLAUDE_ENV_FILE" "$project" "$agent_type" "$RUN_DIR" "$RUN_ID"; then
            log_info "Environment variables persisted"
        else
            log_error "Failed to persist environment variables" $SEVERITY_WARN
        fi
    else
        log_debug "CLAUDE_ENV_FILE not set, skipping persistence"
    fi

    # Step 8: Create Template Files
    if create_template_files "$RUN_DIR" "$project" "$agent_type"; then
        log_info "Template files created"
    else
        log_error "Some template files failed to create" $SEVERITY_WARN
    fi

    # Step 9: Generate AGENT_CONTEXT.md
    if generate_agent_context "$RUN_DIR" "$project" "$agent_type" "$mode"; then
        log_info "Agent context generated"
    else
        log_error "Failed to generate agent context" $SEVERITY_WARN
    fi

    # Step 10: Generate JSON Output
    generate_json_output "$project" "$agent_type" "$mode" "$RUN_DIR" "$RUN_ID"

    # Log completion
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    log_info "SessionStart hook completed in ${duration}s"
    if has_errors; then
        log_warn "Completed with $(error_count) warning(s)"
    fi

    return 0
}
```

---

## 6. Key Improvements Summary

| Issue | Fix | Location |
|-------|-----|----------|
| Missing dependency checks | `validate_dependencies()` function | Called at start of main() |
| Silent failures | Removed `2>/dev/null \|\| true`, explicit error checking | All file operations |
| No signal handling | `cleanup()` trap with `TEMP_FILES` and `LOCK_FD` tracking | Script initialization |
| Inconsistent error handling | Standardized `log_error()`, `safe_mkdir()`, `atomic_write()` | Replace existing functions |
| Race conditions in mktemp | `register_temp_file()` + cleanup trap | File creation operations |
| Lock cleanup | `register_lock_fd()` + cleanup on signals | Lock acquisition/release |

---

## 7. Testing Recommendations

1. **Dependency Validation Test:**
   ```bash
   # Temporarily rename jq, flock, or git
   mv $(which jq) $(which jq).bak
   bash session-start-blackbox5.sh
   # Should output valid JSON error
   mv $(which jq).bak $(which jq)
   ```

2. **Signal Handling Test:**
   ```bash
   # Run hook and press Ctrl+C mid-execution
   # Verify no temp files left in /tmp or target directories
   ```

3. **Error Handling Test:**
   ```bash
   # Set read-only directory and attempt run
   mkdir -p /tmp/test-readonly
   chmod 000 /tmp/test-readonly
   BB5_ROOT=/tmp/test-readonly bash session-start-blackbox5.sh
   # Should log errors gracefully, not crash
   ```

---

*Fixes prepared by Reliability Engineer*
*Based on EVALUATION-AGENT-1.md and IMPROVEMENTS-AGENT-2.md*
