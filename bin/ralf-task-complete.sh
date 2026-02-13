#!/bin/bash
# RALF Task Completion Script
#
# Validates task completion, moves task to completed/, and updates STATE.yaml
#
# Usage: ./ralf-task-complete.sh <task_id>
#
# Arguments:
#   task_id  - Required: Task ID to complete (e.g., TASK-001)
#
# Example:
#   ./ralf-task-complete.sh TASK-1769978192
#

set -euo pipefail

# Script location
BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
TASKS_ACTIVE_DIR="$BB5_DIR/5-project-memory/blackbox5/tasks/active"
TASKS_COMPLETED_DIR="$BB5_DIR/5-project-memory/blackbox5/tasks/completed"
TASKS_WORKING_DIR="$BB5_DIR/5-project-memory/blackbox5/tasks/working"
STATE_FILE="$BB5_DIR/5-project-memory/blackbox5/STATE.yaml"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[TASK-COMPLETE]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[TASK-COMPLETE]${NC} ✅ $1"
}

log_warning() {
    echo -e "${YELLOW}[TASK-COMPLETE]${NC} ⚠️  $1"
}

log_error() {
    echo -e "${RED}[TASK-COMPLETE]${NC} ❌ $1"
}

# Validate arguments
if [ $# -lt 1 ]; then
    log_error "Missing required argument: task_id"
    echo ""
    echo "Usage: $0 <task_id>"
    echo ""
    echo "Example:"
    echo "  $0 TASK-001"
    exit 1
fi

TASK_ID="$1"

# Validate task ID format
if [[ ! "$TASK_ID" =~ ^TASK-[0-9]+$ ]] && [[ ! "$TASK_ID" =~ ^TASK-[A-Z0-9-]+$ ]]; then
    log_error "Invalid task ID format: ${TASK_ID}"
    log_error "Expected format: TASK-001 or TASK-ABC-123"
    exit 1
fi

log_info "Processing task completion for ${TASK_ID}"
echo ""

# Find task directory (could be in active/ or working/)
TASK_DIR=""
if [ -d "$TASKS_WORKING_DIR/$TASK_ID" ]; then
    TASK_DIR="$TASKS_WORKING_DIR/$TASK_ID"
    log_info "Found task in working/ directory"
elif [ -d "$TASKS_ACTIVE_DIR/$TASK_ID" ]; then
    TASK_DIR="$TASKS_ACTIVE_DIR/$TASK_ID"
    log_info "Found task in active/ directory"
else
    log_error "Task directory not found: ${TASK_ID}"
    log_error "Searched in:"
    log_error "  - $TASKS_WORKING_DIR/$TASK_ID"
    log_error "  - $TASKS_ACTIVE_DIR/$TASK_ID"
    exit 1
fi

TASK_FILE="$TASK_DIR/task.md"

# Check if task.md exists
if [ ! -f "$TASK_FILE" ]; then
    log_error "task.md not found: ${TASK_FILE}"
    exit 1
fi

log_info "Task file: ${TASK_FILE}"
echo ""

# Extract task status
TASK_STATUS=$(grep -i "^**Status:**" "$TASK_FILE" | sed 's/**Status:**//I' | xargs || echo "unknown")

log_info "Current status: ${TASK_STATUS}"
echo ""

# Validate task completion

# Check 1: Task should not already be completed
if [[ "$TASK_STATUS" == "completed" ]]; then
    log_warning "Task is already marked as completed"
    log_warning "To re-complete, update task.md status first"
    exit 0
fi

# Check 2: Verify RESULTS.md exists (or is mentioned in deliverables)
RESULTS_CHECK=false
if [ -f "$TASK_DIR/RESULTS.md" ]; then
    log_success "✓ RESULTS.md exists"
    RESULTS_CHECK=true
else
    log_warning "⚠  RESULTS.md not found (may be optional for this task)"
fi

# Check 3: Verify success criteria are met
SUCCESS_COUNT=$(grep -c "^\- \[x\]" "$TASK_FILE" || echo "0")
TOTAL_COUNT=$(grep -c "^\- \[[ x]\]" "$TASK_FILE" || echo "0")

log_info "Success criteria: ${SUCCESS_COUNT}/${TOTAL_COUNT} completed"

if [ "$TOTAL_COUNT" -gt 0 ] && [ "$SUCCESS_COUNT" -lt "$TOTAL_COUNT" ]; then
    log_warning "⚠  Not all success criteria are marked complete"
    log_warning "Proceeding anyway (manual validation required)"
elif [ "$SUCCESS_COUNT" -ge "$TOTAL_COUNT" ]; then
    log_success "✓ All success criteria met"
fi

echo ""

# Confirm before proceeding
read -p "Complete task ${TASK_ID}? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_info "Task completion cancelled"
    exit 0
fi

echo ""

# Step 1: Update task.md status to completed
log_info "Updating task.md status to 'completed'..."

if grep -q "^**Status:**" "$TASK_FILE"; then
    sed -i 's/\*\*Status:\*\*.*/\*\*Status:\*\* completed/' "$TASK_FILE"
    log_success "✓ Status updated"
else
    log_warning "⚠  No '**Status:**' field found, adding one"
    sed -i '1,/^---$/{
        /^---$/i\
**Status:** completed
    }' "$TASK_FILE"
    log_success "✓ Status field added"
fi

# Step 2: Move task to completed/
log_info "Moving task to completed/ directory..."

mkdir -p "$TASKS_COMPLETED_DIR"

mv "$TASK_DIR" "$TASKS_COMPLETED_DIR/$TASK_ID"
log_success "✓ Task moved to ${TASKS_COMPLETED_DIR}/${TASK_ID}"

# Step 3: Update STATE.yaml
log_info "Updating STATE.yaml..."

if [ -f "$STATE_FILE" ]; then
    # STATE.yaml is dynamically derived, no manual update needed
    log_info "ℹ️  STATE.yaml is dynamically derived, no manual update required"
else
    log_warning "⚠  STATE.yaml not found: ${STATE_FILE}"
fi

echo ""

# Summary
log_success "Task ${TASK_ID} completed successfully!"
echo ""
log_info "Task location: ${TASKS_COMPLETED_DIR}/${TASK_ID}"
log_info "Next steps:"
log_info "  1. Verify task results: cat ${TASKS_COMPLETED_DIR}/${TASK_ID}/RESULTS.md"
log_info "  2. Run post-task-completion hook: ${BB5_DIR}/.autonomous/hooks/post-task-complete.sh ${TASK_ID}"
log_info "  3. Commit changes: git add -A && git commit -m 'Complete ${TASK_ID}'"
echo ""

exit 0
