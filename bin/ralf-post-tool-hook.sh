#!/bin/bash
# RALF PostToolUse Hook - File Modification Detection
#
# This hook runs after each tool use during agent execution and:
# 1. Detects task file modifications
# 2. Tracks which files were changed
# 3. Flags for queue sync if task status changed
# 4. Logs tool usage for audit trail
#
# Enforcement: Code-guaranteed (0ms LLM involvement)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
BLACKBOX5_HOME="${BLACKBOX5_HOME:-/opt/blackbox5}"
PROJECT_NAME="${PROJECT_NAME:-blackbox5}"
PROJECT_DIR="${BLACKBOX5_HOME}/5-project-memory/${PROJECT_NAME}"
AUTONOMOUS_DIR="${PROJECT_DIR}/.autonomous"
RUN_DIR="${RUN_DIR:-}"
TASKS_ACTIVE_DIR="${PROJECT_DIR}/tasks/active"
TASKS_WORKING_DIR="${PROJECT_DIR}/tasks/working"
MODIFICATION_LOG="${AUTONOMOUS_DIR}/logs/modifications.log"

log() {
    echo -e "${GREEN}[PostToolHook]${NC} $1" >&2
}

warn() {
    echo -e "${YELLOW}[PostToolHook]${NC} $1" >&2
}

error() {
    echo -e "${RED}[PostToolHook]${NC} $1" >&2
}

info() {
    echo -e "${BLUE}[PostToolHook]${NC} $1" >&2
}

# Create modification log directory
ensure_log_dir() {
    mkdir -p "$(dirname "$MODIFICATION_LOG")"
}

# Track file modifications
track_modification() {
    local file_path="$1"
    local tool_name="$2"

    # Only track files within project directory
    if [[ ! "$file_path" =~ ^"$PROJECT_DIR" ]]; then
        return 0
    fi

    # Skip certain file types (logs, temp files, etc.)
    if [[ "$file_path" =~ \.log$ || "$file_path" =~ \.tmp$ || "$file_path" =~ \.swp$ ]]; then
        return 0
    fi

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local relative_path="${file_path#$PROJECT_DIR/}"

    # Log modification
    echo "$timestamp|$tool_name|$relative_path" >> "$MODIFICATION_LOG"

    log "Modified: $relative_path (tool: $tool_name)"
}

# Check if task status file was modified
check_task_status_change() {
    local modified_files=()

    # Read recent modifications (last 10 entries)
    if [[ -f "$MODIFICATION_LOG" ]]; then
        mapfile -t recent_mods < <(tail -10 "$MODIFICATION_LOG")

        for mod in "${recent_mods[@]}"; do
            local file_path=$(echo "$mod" | cut -d'|' -f3)
            local full_path="${PROJECT_DIR}/${file_path}"

            # Check if it's a task.md file
            if [[ "$file_path" =~ tasks/(active|working)/.+/task\.md$ ]]; then
                modified_files+=("$full_path")
            fi
        done
    fi

    # If task.md files were modified, flag for sync
    if [[ ${#modified_files[@]} -gt 0 ]]; then
        local sync_flag="${AUTONOMOUS_DIR}/.needs_queue_sync"
        touch "$sync_flag"
        log "Task files modified - queue sync needed"
    fi
}

# Check for task file moves (e.g., active -> working)
check_task_moves() {
    # This would be handled by looking at git diff or monitoring directory changes
    # For now, we'll rely on the .needs_queue_sync flag
    :
}

# Generate modification summary for the session
generate_modification_summary() {
    if [[ -n "$RUN_DIR" && -f "$MODIFICATION_LOG" ]]; then
        local run_timestamp=$(basename "$RUN_DIR" | sed 's/run-//')
        local session_mods=0

        # Count modifications since session start
        if [[ -f "$MODIFICATION_LOG" ]]; then
            session_mods=$(grep -c "^${run_timestamp:0:10}" "$MODIFICATION_LOG" || echo "0")
        fi

        # Store summary in run directory
        if [[ -d "$RUN_DIR" ]]; then
            echo "# File Modifications" > "$RUN_DIR/MODIFICATIONS.md"
            echo "" >> "$RUN_DIR/MODIFICATIONS.md"
            echo "Total modifications this session: $session_mods" >> "$RUN_DIR/MODIFICATIONS.md"
            echo "" >> "$RUN_DIR/MODIFICATIONS.md"
            echo "## Recent Changes" >> "$RUN_DIR/MODIFICATIONS.md"

            # Get recent modifications
            if [[ -f "$MODIFICATION_LOG" ]]; then
                tail -20 "$MODIFICATION_LOG" | while IFS='|' read -r timestamp tool file; do
                    echo "- **${timestamp}** - ${tool}: ${file}" >> "$RUN_DIR/MODIFICATIONS.md"
                done
            fi

            log "Modification summary generated: MODIFICATIONS.md"
        fi
    fi
}

# Main execution
main() {
    local tool_name="${1:-unknown}"
    local tool_args="${2:-}"

    log "PostToolUse hook triggered: $tool_name"

    # Ensure log directory exists
    ensure_log_dir

    # Process tool arguments to detect file operations
    case "$tool_name" in
        write_file|edit_file|create_file)
            # Extract file path from arguments
            local file_path=$(echo "$tool_args" | grep -oP '"file_path":"[^"]+' | sed 's/"file_path":"//')
            if [[ -n "$file_path" ]]; then
                track_modification "$file_path" "$tool_name"
            fi
            ;;
        execute_command)
            # Track command execution
            log "Command executed: $tool_args"
            ;;
        read_file)
            # Read operations are not tracked as modifications
            ;;
        *)
            # Other tools
            log "Tool: $tool_name"
            ;;
    esac

    # Check for task status changes
    check_task_status_change

    # Generate periodic modification summary (every 10th call, roughly)
    # This is a simple heuristic - could be improved with counters
    if [[ -f "$RUN_DIR" ]]; then
        local counter_file="${RUN_DIR}/.post_tool_counter"
        local counter=0

        if [[ -f "$counter_file" ]]; then
            counter=$(cat "$counter_file")
        fi

        counter=$((counter + 1))
        echo "$counter" > "$counter_file"

        # Generate summary every 10 tool uses
        if [[ $counter -eq 10 ]] || [[ $counter -eq 50 ]] || [[ $counter -eq 100 ]]; then
            generate_modification_summary
        fi
    fi

    # Return success
    exit 0
}

# Run main function
main "$@"
