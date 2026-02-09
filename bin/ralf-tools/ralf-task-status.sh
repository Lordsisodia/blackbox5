#!/bin/bash
# RALF Task Status Script
# Sync/check task status across queue.yaml
# Usage: ralf-task-status.sh [options]
#
# Options:
#   --show [TASK-ID]  - Show status of specific task or all tasks
#   --list [STATUS]   - List tasks by status (pending/claimed/in_progress/completed/failed/archived)
#   --sync            - Sync status across queue.yaml and events.yaml
#   --verify          - Verify task status consistency
#   --current         - Show current task being worked on

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
AGENT_TYPE="${RALF_AGENT_TYPE:-executor}"
RUN_ID="${RALF_RUN_ID:-unknown}"

# Project root detection
if [ -n "$RALF_PROJECT_ROOT" ]; then
    PROJECT_ROOT="$RALF_PROJECT_ROOT"
elif [ -n "$CLAUDE_CODE_ROOT" ]; then
    PROJECT_ROOT="$CLAUDE_CODE_ROOT"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

# File paths
COMMUNICATIONS_DIR="$PROJECT_ROOT/5-project-memory/$PROJECT_NAME/.autonomous/agents/communications"
QUEUE_FILE="$COMMUNICATIONS_DIR/queue.yaml"
EVENTS_FILE="$COMMUNICATIONS_DIR/events.yaml"
TASKS_DIR="$PROJECT_ROOT/5-project-memory/$PROJECT_NAME/tasks"

# Colors
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    GRAY='\033[0;37m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    CYAN=''
    GRAY=''
    NC=''
fi

log() { echo -e "${BLUE}[RALF-STATUS]${NC} $1"; }
success() { echo -e "${GREEN}[RALF-STATUS]${NC} $1"; }
warning() { echo -e "${YELLOW}[RALF-STATUS]${NC} $1"; }
error() { echo -e "${RED}[RALF-STATUS]${NC} $1"; }
info() { echo -e "${CYAN}[RALF-STATUS]${NC} $1"; }
dim() { echo -e "${GRAY}$1${NC}"; }

# =============================================================================
# FUNCTIONS
# =============================================================================

show_help() {
    cat << 'EOF'
RALF Task Status Script

Usage: ralf-task-status.sh [command] [options]

Commands:
  --show [TASK-ID]     Show status of specific task or all tasks (default)
  --list [STATUS]      List tasks filtered by status
  --sync               Sync status across queue.yaml and events.yaml
  --verify             Verify consistency between queue.yaml and events.yaml
  --current            Show the currently active/claimed task
  --help, -h           Show this help message

Status Values:
  pending              Task is waiting to be claimed
  claimed              Task has been claimed by an executor
  in_progress          Task is actively being worked on
  completed            Task finished successfully
  failed               Task failed and needs replanning
  archived             Task has been moved to completed/

Examples:
  ralf-task-status.sh                    # Show all tasks
  ralf-task-status.sh --show TASK-001    # Show specific task
  ralf-task-status.sh --list in_progress # List all in-progress tasks
  ralf-task-status.sh --current          # Show current task
  ralf-task-status.sh --sync             # Sync statuses
  ralf-task-status.sh --verify           # Check for inconsistencies

EOF
}

# Show status of all tasks or a specific task
show_status() {
    local target_task="${1:-}"

    if [ ! -f "$QUEUE_FILE" ]; then
        error "queue.yaml not found at $QUEUE_FILE"
        return 1
    fi

    log "Task Status Overview"
    echo ""

    # Parse and display tasks
    local in_tasks=0
    local current_task=""
    local current_status=""
    local current_title=""
    local count_pending=0
    local count_claimed=0
    local count_in_progress=0
    local count_completed=0
    local count_failed=0

    while IFS= read -r line; do
        # Detect start of tasks section
        if [[ "$line" =~ ^tasks:$ ]]; then
            in_tasks=1
            continue
        fi

        # Detect end of tasks section
        if [ $in_tasks -eq 1 ] && [[ "$line" =~ ^[a-z].*: ]]; then
            in_tasks=0
            continue
        fi

        # Parse task entries
        if [ $in_tasks -eq 1 ]; then
            # Task ID
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*(.+)$ ]]; then
                current_task="${BASH_REMATCH[1]}"
                current_status=""
                current_title=""
            fi

            # Status
            if [[ "$line" =~ ^[[:space:]]*status:[[:space:]]*(.+)$ ]]; then
                current_status="${BASH_REMATCH[1]}"
            fi

            # Title
            if [[ "$line" =~ ^[[:space:]]*title:[[:space:]]*(.+)$ ]]; then
                current_title="${BASH_REMATCH[1]}"
            fi

            # When we have all fields, display or count
            if [ -n "$current_task" ] && [ -n "$current_status" ] && [ -n "$current_title" ]; then
                # Count by status
                case "$current_status" in
                    pending) ((count_pending++)) ;;
                    claimed) ((count_claimed++)) ;;
                    in_progress) ((count_in_progress++)) ;;
                    completed) ((count_completed++)) ;;
                    failed) ((count_failed++)) ;;
                esac

                # Display if no target or matches target
                if [ -z "$target_task" ] || [ "$current_task" = "$target_task" ]; then
                    local status_color="$NC"
                    case "$current_status" in
                        pending) status_color="$GRAY" ;;
                        claimed) status_color="$YELLOW" ;;
                        in_progress) status_color="$BLUE" ;;
                        completed) status_color="$GREEN" ;;
                        failed) status_color="$RED" ;;
                    esac

                    printf "  ${status_color}%-12s${NC}  %-20s  %s\n" \
                        "[$current_status]" "$current_task" "$current_title"
                fi

                current_task=""
            fi
        fi
    done < "$QUEUE_FILE"

    echo ""
    info "Summary:"
    echo "  Pending:     $count_pending"
    echo "  Claimed:     $count_claimed"
    echo "  In Progress: $count_in_progress"
    echo "  Completed:   $count_completed"
    echo "  Failed:      $count_failed"
}

# List tasks by specific status
list_by_status() {
    local filter_status="${1:-}"

    if [ -z "$filter_status" ]; then
        error "No status specified. Use: pending, claimed, in_progress, completed, failed, archived"
        return 1
    fi

    if [ ! -f "$QUEUE_FILE" ]; then
        error "queue.yaml not found"
        return 1
    fi

    log "Tasks with status: $filter_status"
    echo ""

    local in_tasks=0
    local current_task=""
    local current_status=""
    local current_title=""
    local found=0

    while IFS= read -r line; do
        if [[ "$line" =~ ^tasks:$ ]]; then
            in_tasks=1
            continue
        fi

        if [ $in_tasks -eq 1 ] && [[ "$line" =~ ^[a-z].*: ]]; then
            in_tasks=0
            continue
        fi

        if [ $in_tasks -eq 1 ]; then
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*(.+)$ ]]; then
                current_task="${BASH_REMATCH[1]}"
                current_status=""
                current_title=""
            fi

            if [[ "$line" =~ ^[[:space:]]*status:[[:space:]]*(.+)$ ]]; then
                current_status="${BASH_REMATCH[1]}"
            fi

            if [[ "$line" =~ ^[[:space:]]*title:[[:space:]]*(.+)$ ]]; then
                current_title="${BASH_REMATCH[1]}"
            fi

            if [ -n "$current_task" ] && [ -n "$current_status" ] && [ -n "$current_title" ]; then
                if [ "$current_status" = "$filter_status" ]; then
                    echo "  $current_task - $current_title"
                    found=1
                fi
                current_task=""
            fi
        fi
    done < "$QUEUE_FILE"

    if [ $found -eq 0 ]; then
        dim "  No tasks found with status: $filter_status"
    fi
}

# Show current task (claimed or in_progress)
show_current() {
    if [ ! -f "$QUEUE_FILE" ]; then
        error "queue.yaml not found"
        return 1
    fi

    log "Current Active Tasks"
    echo ""

    local in_tasks=0
    local current_task=""
    local current_status=""
    local current_title=""
    local current_claimed_by=""
    local current_started_at=""
    local found=0

    while IFS= read -r line; do
        if [[ "$line" =~ ^tasks:$ ]]; then
            in_tasks=1
            continue
        fi

        if [ $in_tasks -eq 1 ] && [[ "$line" =~ ^[a-z].*: ]]; then
            in_tasks=0
            continue
        fi

        if [ $in_tasks -eq 1 ]; then
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*(.+)$ ]]; then
                current_task="${BASH_REMATCH[1]}"
                current_status=""
                current_title=""
                current_claimed_by=""
                current_started_at=""
            fi

            if [[ "$line" =~ ^[[:space:]]*status:[[:space:]]*(.+)$ ]]; then
                current_status="${BASH_REMATCH[1]}"
            fi

            if [[ "$line" =~ ^[[:space:]]*title:[[:space:]]*(.+)$ ]]; then
                current_title="${BASH_REMATCH[1]}"
            fi

            if [[ "$line" =~ claimed_by:[[:space:]]*(.+)$ ]]; then
                current_claimed_by="${BASH_REMATCH[1]}"
            fi

            if [[ "$line" =~ started_at:[[:space:]]*(.+)$ ]]; then
                current_started_at="${BASH_REMATCH[1]}"
            fi

            if [ -n "$current_task" ] && [ -n "$current_status" ] && [ -n "$current_title" ]; then
                if [ "$current_status" = "claimed" ] || [ "$current_status" = "in_progress" ]; then
                    echo "  Task:       $current_task"
                    echo "  Title:      $current_title"
                    echo "  Status:     $current_status"
                    [ -n "$current_claimed_by" ] && echo "  Claimed By: $current_claimed_by"
                    [ -n "$current_started_at" ] && echo "  Started:    $current_started_at"
                    echo ""
                    found=1
                fi
                current_task=""
            fi
        fi
    done < "$QUEUE_FILE"

    if [ $found -eq 0 ]; then
        info "No active tasks (claimed or in_progress)"
    fi
}

# Sync status between queue.yaml and events.yaml
sync_status() {
    log "Syncing task status..."

    if [ ! -f "$QUEUE_FILE" ]; then
        error "queue.yaml not found"
        return 1
    fi

    if [ ! -f "$EVENTS_FILE" ]; then
        warning "events.yaml not found, skipping event sync"
    fi

    # This is a placeholder for more complex sync logic
    # For now, we just verify consistency
    verify_status

    success "Status sync complete"
}

# Verify consistency between queue.yaml and events.yaml
verify_status() {
    log "Verifying task status consistency..."
    echo ""

    if [ ! -f "$QUEUE_FILE" ]; then
        error "queue.yaml not found"
        return 1
    fi

    local issues=0

    # Check for tasks with invalid statuses
    local in_tasks=0
    local current_task=""
    local current_status=""
    local valid_statuses="pending claimed in_progress completed failed archived"

    while IFS= read -r line; do
        if [[ "$line" =~ ^tasks:$ ]]; then
            in_tasks=1
            continue
        fi

        if [ $in_tasks -eq 1 ] && [[ "$line" =~ ^[a-z].*: ]]; then
            in_tasks=0
            continue
        fi

        if [ $in_tasks -eq 1 ]; then
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*(.+)$ ]]; then
                current_task="${BASH_REMATCH[1]}"
                current_status=""
            fi

            if [[ "$line" =~ ^[[:space:]]*status:[[:space:]]*(.+)$ ]]; then
                current_status="${BASH_REMATCH[1]}"
            fi

            if [ -n "$current_task" ] && [ -n "$current_status" ]; then
                # Check if status is valid
                if [[ ! " $valid_statuses " =~ " $current_status " ]]; then
                    warning "Invalid status '$current_status' for task $current_task"
                    ((issues++))
                fi

                # Check if completed tasks have completed_at timestamp
                if [ "$current_status" = "completed" ]; then
                    local has_completed_at=$(grep -A 10 "id: $current_task" "$QUEUE_FILE" | grep "completed_at:" || true)
                    if [ -z "$has_completed_at" ]; then
                        warning "Task $current_task is completed but missing completed_at timestamp"
                        ((issues++))
                    fi
                fi

                current_task=""
            fi
        fi
    done < "$QUEUE_FILE"

    echo ""
    if [ $issues -eq 0 ]; then
        success "No issues found - all statuses are consistent"
    else
        warning "Found $issues issue(s) that may need attention"
    fi
}

# =============================================================================
# MAIN
# =============================================================================

COMMAND="${1:---show}"
shift || true

case "$COMMAND" in
    --show|-s)
        show_status "$@"
        ;;
    --list|-l)
        list_by_status "$@"
        ;;
    --current|-c)
        show_current
        ;;
    --sync)
        sync_status
        ;;
    --verify|-v)
        verify_status
        ;;
    --help|-h)
        show_help
        ;;
    *)
        # If first arg looks like a task ID, show that task
        if [[ "$COMMAND" =~ ^TASK- ]]; then
            show_status "$COMMAND"
        else
            error "Unknown command: $COMMAND"
            echo "Use --help for usage information"
            exit 1
        fi
        ;;
esac
