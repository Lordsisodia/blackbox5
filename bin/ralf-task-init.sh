#!/bin/bash
# RALF Task Working Directory Initialization
# Phase 4 implementation - Creates task execution context
#
# Usage: ralf-task-init.sh --task-id TASK-XXX [--run-id RUN-YYY]

set -e

# Configuration
PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
AGENT_TYPE="${RALF_AGENT_TYPE:-executor}"
RUN_ID="${RALF_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"

# Project root detection
if [ -n "$RALF_PROJECT_ROOT" ]; then
    PROJECT_ROOT="$RALF_PROJECT_ROOT"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

# Paths
PROJECT_MEMORY="$PROJECT_ROOT/5-project-memory/$PROJECT_NAME"
TASKS_DIR="$PROJECT_MEMORY/tasks"
WORKING_DIR="$TASKS_DIR/working"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[TASK-INIT]${NC} $1"; }
success() { echo -e "${GREEN}[TASK-INIT]${NC} $1"; }

# Main
create_working_directory() {
    local task_id="$1"
    local run_id="${2:-$RUN_ID}"

    local task_working_dir="$WORKING_DIR/$task_id/$run_id"

    log "Creating task working directory: $task_working_dir"
    mkdir -p "$task_working_dir"

    # Create README.md
    cat > "$task_working_dir/README.md" << EOF
# Task Execution: $task_id

**Run ID:** $run_id
**Agent:** $AGENT_TYPE
**Started:** $(date -Iseconds)

## Goal
[To be filled from task.md]

## Progress
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Status
🟡 In Progress
EOF

    # Create TASK-CONTEXT.md (read-only reference)
    cat > "$task_working_dir/TASK-CONTEXT.md" << EOF
# Task Context: $task_id

**Source:** $TASKS_DIR/active/$task_id/task.md

## Specification
[Auto-populated from task.md on first read]

## Dependencies
[List from task.md]

## Acceptance Criteria
[From task.md success criteria]
EOF

    # Create ACTIVE-CONTEXT.md (executor writes here)
    cat > "$task_working_dir/ACTIVE-CONTEXT.md" << EOF
# Active Context: $task_id

**Executor:** $AGENT_TYPE
**Run:** $run_id

## Discoveries

## Deviations from Plan

## Blockers

## Questions for Planner

## Verification Evidence
EOF

    # Create link to run folder
    if [ -d "$PROJECT_MEMORY/runs/$AGENT_TYPE/$run_id" ]; then
        ln -sf "$PROJECT_MEMORY/runs/$AGENT_TYPE/$run_id" "$task_working_dir/run"
    fi

    # Export for environment
    export RALF_TASK_WORKING_DIR="$task_working_dir"

    success "Task working directory created"
    echo "RALF_TASK_WORKING_DIR=$task_working_dir"
}

# Parse arguments
TASK_ID=""
RUN_ID=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --task-id)
            TASK_ID="$2"
            shift 2
            ;;
        --run-id)
            RUN_ID="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "$TASK_ID" ]; then
    echo "Usage: $0 --task-id TASK-XXX [--run-id RUN-YYY]"
    exit 1
fi

create_working_directory "$TASK_ID" "$RUN_ID"
