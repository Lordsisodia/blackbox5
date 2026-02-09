#!/bin/bash
# RALF Task Selection Script
# Phase 3 implementation - Executor calls this to claim tasks
# This is a COMMAND script - runs bash directly, zero LLM tokens
#
# Usage: ralf-task-select.sh [options]
#   Options:
#     --claim    - Claim the next task from queue.yaml
#     --status   - Show current queue status
#     --idle     - Report idle status (no task available)

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
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

# Source libraries
source "${SCRIPT_DIR}/../../2-engine/helpers/legacy/paths.sh"
source "${SCRIPT_DIR}/../../2-engine/helpers/legacy/error_handler.sh"

# File paths
COMMUNICATIONS_DIR="$(get_project_path)/.autonomous/agents/communications"
HEARTBEAT_FILE="$COMMUNICATIONS_DIR/heartbeat.yaml"
QUEUE_FILE="$COMMUNICATIONS_DIR/queue.yaml"
EVENTS_FILE="$COMMUNICATIONS_DIR/events.yaml"
TASKS_FILE="$COMMUNICATIONS_DIR/tasks.yaml"

# Ensure communications directory exists
if ! eh_dir_exists "$COMMUNICATIONS_DIR" "communications"; then
    eh_ensure_dir "$COMMUNICATIONS_DIR" || {
        log_error "Cannot create communications directory"
        exit 1
    }
fi

# Colors
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    NC=''
fi

log() { echo -e "${BLUE}[RALF-TASK]${NC} $1"; }
log_success() { echo -e "${GREEN}[RALF-TASK]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[RALF-TASK]${NC} $1"; }
log_error() { echo -e "${RED}[RALF-TASK]${NC} $1"; }

# =============================================================================
# FUNCTIONS
# =============================================================================

show_status() {
    log "Current queue status:"
    echo ""

    if ! eh_file_exists "$QUEUE_FILE" "queue status check"; then
        log_warning "queue.yaml not found - queue may be empty or uninitialized"
        echo "  status: uninitialized"
        echo "  queue_depth: 0"
        return 0
    fi

    # Parse queue.yaml
    NEXT_TASK=$(grep "^next_task:" "$QUEUE_FILE" 2>/dev/null | cut -d':' -f2- | tr -d ' "' || echo "null")
    QUEUE_STATUS=$(grep "^status:" "$QUEUE_FILE" 2>/dev/null | cut -d':' -f2- | tr -d ' ' || echo "unknown")
    REASONING=$(grep "^reasoning:" "$QUEUE_FILE" 2>/dev/null | cut -d':' -f2- | sed 's/^ *//' || echo "")

    echo "  next_task: $NEXT_TASK"
    echo "  status: $QUEUE_STATUS"
    echo "  reasoning: $REASONING"
    echo ""

    # Show heartbeat if exists
    if [ -f "$HEARTBEAT_FILE" ]; then
        EXECUTOR_STATUS=$(grep -A 5 "executor:" "$HEARTBEAT_FILE" 2>/dev/null | grep "status:" | cut -d':' -f2- | tr -d ' ' || echo "unknown")
        echo "  executor heartbeat: $EXECUTOR_STATUS"
    fi
}

claim_task() {
    log "Claiming task from queue..."

    if ! eh_file_exists "$QUEUE_FILE" "task claim"; then
        log_warning "queue.yaml not found - creating minimal queue"
        eh_create_minimal_queue "$QUEUE_FILE"
        log_warning "No tasks available in new queue"
        return 2
    fi

    # Read first pending task from queue
    # Queue format: YAML list with task_id and status fields
    # Parse using awk to find task with status: pending
    NEXT_TASK=$(awk -F': ' '/^  - task_id:/{tid=$2}/^    status: pending/{if(tid){print tid;exit}}' "$QUEUE_FILE" 2>/dev/null || echo "")

    # Check if empty
    if [ -z "$NEXT_TASK" ]; then
        log_warning "No pending tasks in queue.yaml"
        return 2
    fi

    log "Found task: $NEXT_TASK"

    # Get task details from tasks.yaml if available
    TASK_TITLE=""
    if eh_file_exists "$TASKS_FILE" "task details lookup"; then
        TASK_TITLE=$(grep -A 20 "id:.*$NEXT_TASK" "$TASKS_FILE" 2>/dev/null | grep "title:" | head -1 | cut -d':' -f2- | sed 's/^ *//' || echo "")
    else
        eh_log_warning "tasks.yaml not found - using task ID as title"
        TASK_TITLE="$NEXT_TASK"
    fi

    TIMESTAMP=$(date -Iseconds)

    # Write claim event to events.yaml with file locking
    if eh_file_exists "$EVENTS_FILE" "event logging"; then
        (
            flock -x 200
            cat >> "$EVENTS_FILE" << EOF

- timestamp: "$TIMESTAMP"
  task_id: "$NEXT_TASK"
  type: started
  agent: executor
  run_id: "$RUN_ID"
EOF
        ) 200>"$COMMUNICATIONS_DIR/.events.lock"
        log_success "Claim event written to events.yaml"
    else
        eh_log_warning "events.yaml not found - claim event not logged"
    fi

    # Update queue.yaml - set task status to claimed (with file locking)
    if eh_file_exists "$QUEUE_FILE" "queue update"; then
        (
            flock -x 200
            # Use awk to update the specific task's status and add claimed timestamps
            awk -F': ' -v task_id="$NEXT_TASK" -v timestamp="$TIMESTAMP" -v run_id="$RUN_ID" '
                /^  - task_id: / {
                    in_target_task = ($2 == task_id)
                }
                in_target_task && /^    status: / {
                    print "    status: claimed"
                    print "    claimed_at: \"" timestamp "\""
                    print "    claimed_by: \"" run_id "\""
                    next
                }
                { print }
            ' "$QUEUE_FILE" > "$QUEUE_FILE.tmp" && mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"

            log_success "Task status updated to 'claimed' in queue.yaml"
        ) 200>"$COMMUNICATIONS_DIR/.queue.lock"
    else
        eh_log_warning "queue.yaml not found - cannot update task status"
    fi

    # Update heartbeat
    if eh_file_exists "$HEARTBEAT_FILE" "heartbeat update"; then
        # Use sed to update executor section
        sed -i.bak "s/last_seen: .*/last_seen: '$TIMESTAMP'/" "$HEARTBEAT_FILE" 2>/dev/null || true
        sed -i.bak "s/status: .*/status: executing/" "$HEARTBEAT_FILE" 2>/dev/null || true
        sed -i.bak "s/current_action: .*/current_action: executing_$NEXT_TASK/" "$HEARTBEAT_FILE" 2>/dev/null || true
        rm -f "$HEARTBEAT_FILE.bak"

        log_success "Heartbeat updated"
    else
        eh_log_warning "heartbeat.yaml not found - cannot update heartbeat"
    fi

    # Create task working directory
    log "Creating task working directory..."
    TASK_WORKING_DIR="$(get_tasks_path)/working/$NEXT_TASK/$RUN_ID"
    mkdir -p "$TASK_WORKING_DIR"

    # Create README.md
    cat > "$TASK_WORKING_DIR/README.md" << EOF
# Task Execution: $NEXT_TASK

**Run ID:** $RUN_ID
**Agent:** $AGENT_TYPE
**Started:** $TIMESTAMP

## Goal
${TASK_TITLE:-$NEXT_TASK}

## Progress
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Status
🟡 In Progress
EOF

    # Create TASK-CONTEXT.md
    cat > "$TASK_WORKING_DIR/TASK-CONTEXT.md" << EOF
# Task Context: $NEXT_TASK

**Source:** tasks/active/$NEXT_TASK/task.md

## Specification
[To be populated from task.md]

## Dependencies
[List from task.md]

## Acceptance Criteria
[From task.md success criteria]
EOF

    # Create ACTIVE-CONTEXT.md
    cat > "$TASK_WORKING_DIR/ACTIVE-CONTEXT.md" << EOF
# Active Context: $NEXT_TASK

**Executor:** $AGENT_TYPE
**Run:** $RUN_ID

## Discoveries

## Deviations from Plan

## Blockers

## Questions for Planner

## Verification Evidence
EOF

    # Link to run folder if it exists
    RUN_DIR="$(get_runs_path)/$AGENT_TYPE/$RUN_ID"
    if [ -d "$RUN_DIR" ]; then
        ln -sf "$RUN_DIR" "$TASK_WORKING_DIR/run"
    fi

    log_success "Task working directory created: $TASK_WORKING_DIR"

    # Output the task ID for the caller
    echo ""
    log_success "Task claimed successfully"
    echo ""
    echo "TASK_ID=$NEXT_TASK"
    if [ -n "$TASK_TITLE" ]; then
        echo "TASK_TITLE=$TASK_TITLE"
    fi
    echo "TASK_WORKING_DIR=$TASK_WORKING_DIR"

    return 0
}

report_idle() {
    log "Reporting idle status..."

    TIMESTAMP=$(date -Iseconds)

    # Write idle event to events.yaml with file locking
    if eh_file_exists "$EVENTS_FILE" "idle event logging"; then
        (
            flock -x 200
            cat >> "$EVENTS_FILE" << EOF

- timestamp: "$TIMESTAMP"
  type: idle
  agent: executor
  run_id: "$RUN_ID"
  reason: "queue.yaml has no next_task"
EOF
        ) 200>"$COMMUNICATIONS_DIR/.events.lock"
        log_success "Idle event written to events.yaml"
    else
        eh_log_warning "events.yaml not found - idle event not logged"
    fi

    # Update heartbeat
    if eh_file_exists "$HEARTBEAT_FILE" "heartbeat update"; then
        sed -i.bak "s/last_seen: .*/last_seen: '$TIMESTAMP'/" "$HEARTBEAT_FILE" 2>/dev/null || true
        sed -i.bak "s/status: .*/status: idle/" "$HEARTBEAT_FILE" 2>/dev/null || true
        sed -i.bak "s/current_action: .*/current_action: waiting_for_task/" "$HEARTBEAT_FILE" 2>/dev/null || true
        rm -f "$HEARTBEAT_FILE.bak"
    else
        eh_log_warning "heartbeat.yaml not found - cannot update heartbeat"
    fi

    echo ""
    log_warning "No task available. Waiting for Planner."
    echo ""

    return 0
}

# =============================================================================
# MAIN
# =============================================================================

COMMAND="${1:---status}"

case "$COMMAND" in
    --status|-s)
        show_status
        ;;
    --claim|-c)
        claim_task
        exit_code=$?
        if [ $exit_code -eq 2 ]; then
            # No task available
            report_idle
            exit 0
        fi
        exit $exit_code
        ;;
    --idle|-i)
        report_idle
        ;;
    --help|-h)
        echo "RALF Task Selection Script"
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  --status, -s    Show current queue status (default)"
        echo "  --claim, -c     Claim the next task from queue"
        echo "  --idle, -i      Report idle status"
        echo "  --help, -h      Show this help"
        echo ""
        echo "Environment variables:"
        echo "  RALF_PROJECT_ROOT    Project root directory"
        echo "  RALF_RUN_ID          Current run ID"
        echo "  RALF_AGENT_TYPE      Agent type (default: executor)"
        ;;
    *)
        log_error "Unknown command: $COMMAND"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
