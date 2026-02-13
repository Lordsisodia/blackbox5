#!/usr/bin/env bash
#
# Post-Task-Completion Hook
#
# This hook is called after a task is completed to automatically sync
# the roadmap state (STATE.yaml, goals.yaml, plan metadata) and
# log skill usage from the task run.
#
# Usage: ./post-task-complete.sh <task_id> [plan_id] [goal_id] [run_dir]
#
# Arguments:
#   task_id  - Required: Completed task ID (e.g., TASK-001)
#   plan_id  - Optional: Plan ID associated with task (e.g., PLAN-001)
#   goal_id  - Optional: Goal ID associated with task (e.g., IG-001)
#   run_dir  - Optional: Run directory containing THOUGHTS.md (e.g., /path/to/run)
#
# Example:
#   ./post-task-complete.sh TASK-001 PLAN-001 IG-001
#   ./post-task-complete.sh TASK-001 PLAN-001 IG-001 /path/to/run
#

set -euo pipefail

# Script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BB5_DIR="/opt/blackbox5"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Validate arguments
if [ $# -lt 1 ]; then
    log_error "Missing required argument: task_id"
    echo ""
    echo "Usage: $0 <task_id> [plan_id] [goal_id] [run_dir]"
    echo ""
    echo "Example:"
    echo "  $0 TASK-001 PLAN-001 IG-001"
    echo "  $0 TASK-001 PLAN-001 IG-001 /path/to/run"
    exit 1
fi

TASK_ID="$1"
PLAN_ID="${2:-}"
GOAL_ID="${3:-}"
RUN_DIR="${4:-}"

log_info "Post-task-completion hook for ${TASK_ID}"
echo ""

# Extract plan_id from task file if not provided
if [ -z "$PLAN_ID" ]; then
    TASK_FILE="${BB5_DIR}/5-project-memory/blackbox5/tasks/active/${TASK_ID}/task.md"

    if [ -f "$TASK_FILE" ]; then
        PLAN_ID=$(grep -i "linked.*plan" "$TASK_FILE" | head -1 | sed 's/.*PLAN-\([0-9]*\).*/PLAN-\1/' || true)
        if [ -n "$PLAN_ID" ]; then
            log_info "Extracted plan_id from task: ${PLAN_ID}"
        fi
    else
        log_warning "Task file not found: ${TASK_FILE}"
    fi
fi

# Extract goal_id from task file if not provided
if [ -z "$GOAL_ID" ]; then
    TASK_FILE="${BB5_DIR}/5-project-memory/blackbox5/tasks/active/${TASK_ID}/task.md"

    if [ -f "$TASK_FILE" ]; then
        GOAL_ID=$(grep -i "linked.*goal" "$TASK_FILE" | head -1 | sed 's/.*IG-\([0-9]*\).*/IG-\1/' || true)
        if [ -n "$GOAL_ID" ]; then
            log_info "Extracted goal_id from task: ${GOAL_ID}"
        fi
    fi
fi

# Call the roadmap sync script
log_info "Synchronizing roadmap state..."

SYNC_SCRIPT="${BB5_DIR}/.autonomous/lib/roadmap_sync.py"

if [ ! -f "$SYNC_SCRIPT" ]; then
    log_error "Roadmap sync script not found: ${SYNC_SCRIPT}"
    exit 1
fi

# Execute sync
if [ -n "$PLAN_ID" ] && [ -n "$GOAL_ID" ]; then
    python3 "$SYNC_SCRIPT" "$TASK_ID" "$PLAN_ID" "$GOAL_ID"
elif [ -n "$PLAN_ID" ]; then
    python3 "$SYNC_SCRIPT" "$TASK_ID" "$PLAN_ID"
else
    python3 "$SYNC_SCRIPT" "$TASK_ID"
fi

SYNC_EXIT_CODE=$?

echo ""

if [ $SYNC_EXIT_CODE -eq 0 ]; then
    log_success "Roadmap synchronization completed"
else
    log_error "Roadmap synchronization failed with exit code ${SYNC_EXIT_CODE}"
    exit $SYNC_EXIT_CODE
fi

# Log skill usage if run directory is provided
if [ -n "$RUN_DIR" ] && [ -d "$RUN_DIR" ]; then
    log_info "Logging skill usage..."

    SKILL_LOG_SCRIPT="${BB5_DIR}/5-project-memory/blackbox5/.claude/hooks/log-skill-on-complete.py"

    if [ ! -f "$SKILL_LOG_SCRIPT" ]; then
        log_warning "Skill logging script not found: ${SKILL_LOG_SCRIPT}"
    else
        # Call skill logging script
        python3 "$SKILL_LOG_SCRIPT" --run-dir "$RUN_DIR" --task-id "$TASK_ID" || {
            log_warning "Skill usage logging failed (non-critical)"
        }
    fi
else
    log_info "No run directory provided, skipping skill usage logging"
fi

log_success "Post-task-completion hook finished"
echo ""

exit 0
