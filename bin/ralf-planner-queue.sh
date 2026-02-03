#!/bin/bash
# RALF Planner Queue Automation
# Automatically populates queue.yaml with prioritized tasks
# Usage: ralf-planner-queue.sh [--check | --fill]

set -e

# Configuration
PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
AGENT_TYPE="${RALF_AGENT_TYPE:-planner}"
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
TASKS_DIR="$PROJECT_MEMORY/tasks/active"
QUEUE_FILE="$PROJECT_MEMORY/.autonomous/agents/communications/queue.yaml"
EVENTS_FILE="$PROJECT_MEMORY/.autonomous/agents/communications/events.yaml"

# Queue settings
QUEUE_DEPTH_TARGET_MIN=3
QUEUE_DEPTH_TARGET_MAX=5

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[PLANNER-QUEUE]${NC} $1"; }
success() { echo -e "${GREEN}[PLANNER-QUEUE]${NC} $1"; }
warning() { echo -e "${YELLOW}[PLANNER-QUEUE]${NC} $1"; }

# Calculate priority score for a task
calculate_priority_score() {
    local task_file="$1"

    # Parse priority from task file
    local priority="medium"
    if grep -q "Priority:.*critical" "$task_file" 2>/dev/null; then
        priority="critical"
    elif grep -q "Priority:.*high" "$task_file" 2>/dev/null; then
        priority="high"
    elif grep -q "Priority:.*low" "$task_file" 2>/dev/null; then
        priority="low"
    fi

    # Parse estimated lines
    local estimated_lines="$(grep -E "Estimated Lines:" "$task_file" | head -1 | grep -oE "[0-9]+" | head -1 || echo "1000")"
    if [ -z "$estimated_lines" ]; then
        estimated_lines=1000
    fi

    # Base score by priority
    local base_score=5
    case "$priority" in
        critical) base_score=10 ;;
        high) base_score=7 ;;
        medium) base_score=5 ;;
        low) base_score=3 ;;
    esac

    # Calculate ROI score (higher impact, lower effort = higher score)
    local effort_bonus=0
    if [ "$estimated_lines" -lt 500 ]; then
        effort_bonus=3
    elif [ "$estimated_lines" -lt 1500 ]; then
        effort_bonus=1
    fi

    local score=$((base_score + effort_bonus))

    # Output: TASK_ID|SCORE|TITLE|PRIORITY|LINES
    local task_id="$(basename "$(dirname "$task_file")")"
    local title="$(grep "^# " "$task_file" | head -1 | sed 's/^# //' || echo "Unknown")"

    echo "$task_id|$score|$title|$priority|$estimated_lines"
}

# Check current queue depth
check_queue_depth() {
    if [ ! -f "$QUEUE_FILE" ]; then
        echo "0"
        return
    fi

    # Count pending tasks in queue
    awk '/^  - task_id:/{task=1} /^    status: pending/{pending++} END{print pending+0}' "$QUEUE_FILE"
}

# Get pending tasks from tasks/active/
get_pending_tasks() {
    local pending_tasks=""

    for task_dir in "$TASKS_DIR"/TASK-*; do
        [ -d "$task_dir" ] || continue

        local task_file="$task_dir/task.md"
        [ -f "$task_file" ] || continue

        # Check if task is pending
        local status=$(grep -E "^\\*\\*Status:\\*\\*" "$task_file" | head -1 | sed 's/.*: \\([^\\*]*\\).*/\\1/' | tr -d ' ' || echo "pending")

        if [ "$status" = "pending" ] || [ -z "$status" ]; then
            local score_info=$(calculate_priority_score "$task_file")
            pending_tasks="$pending_tasks\\n$score_info"
        fi
    done

    # Sort by score (descending), output sorted list
    echo -e "$pending_tasks" | grep -v "^$" | sort -t'|' -k2 -nr
}

# Add task to queue
add_task_to_queue() {
    local task_info="$1"
    local task_id=$(echo "$task_info" | cut -d'|' -f1)
    local score=$(echo "$task_info" | cut -d'|' -f2)
    local title=$(echo "$task_info" | cut -d'|' -f3)
    local priority=$(echo "$task_info" | cut -d'|' -f4)
    local lines=$(echo "$task_info" | cut -d'|' -f5)

    local timestamp=$(date -Iseconds)
    local estimated_minutes=$((lines / 500))  # Rough estimate: 500 lines/min

    # Append to queue.yaml
    cat >> "$QUEUE_FILE" << EOF
  - task_id: $task_id
    priority: $priority
    priority_score: $score
    estimated_minutes: $estimated_minutes
    estimated_lines: $lines
    status: pending
    created_at: "$timestamp"
    notes: "$title"
EOF

    success "Added $task_id to queue (score: $score)"
}

# Fill queue to target depth
fill_queue() {
    log "Checking queue depth..."

    local current_depth=$(check_queue_depth)
    log "Current queue depth: $current_depth"

    if [ "$current_depth" -ge "$QUEUE_DEPTH_TARGET_MIN" ]; then
        success "Queue depth is healthy ($current_depth >= $QUEUE_DEPTH_TARGET_MIN)"
        return 0
    fi

    local needed=$((QUEUE_DEPTH_TARGET_MIN - current_depth))
    log "Queue needs $needed more task(s)"

    # Get pending tasks sorted by priority
    log "Scanning for pending tasks..."
    local pending_tasks=$(get_pending_tasks)

    if [ -z "$pending_tasks" ]; then
        warning "No pending tasks found in $TASKS_DIR"
        return 1
    fi

    # Add highest priority tasks to queue
    local added=0
    echo "$pending_tasks" | while read -r task_info && [ $added -lt $needed ]; do
        [ -n "$task_info" ] || continue

        local task_id=$(echo "$task_info" | cut -d'|' -f1)

        # Check if task already in queue
        if grep -q "task_id: $task_id" "$QUEUE_FILE" 2>/dev/null; then
            log "Task $task_id already in queue, skipping"
            continue
        fi

        add_task_to_queue "$task_info"
        added=$((added + 1))
    done

    # Update metadata
    local new_depth=$(check_queue_depth)
    local timestamp=$(date -Iseconds)

    # Update or add metadata section
    if grep -q "^metadata:" "$QUEUE_FILE"; then
        # Update existing metadata
        sed -i.bak "s/last_updated: .*/last_updated: \"$timestamp\"/" "$QUEUE_FILE"
        sed -i.bak "s/updated_by: .*/updated_by: planner-$RUN_ID/" "$QUEUE_FILE"
        sed -i.bak "s/current_depth: .*/current_depth: $new_depth/" "$QUEUE_FILE"
        rm -f "$QUEUE_FILE.bak"
    else
        # Add metadata section
        cat >> "$QUEUE_FILE" << EOF

metadata:
  last_updated: "$timestamp"
  updated_by: planner-$RUN_ID
  queue_depth_target: $QUEUE_DEPTH_TARGET_MIN-$QUEUE_DEPTH_TARGET_MAX
  current_depth: $new_depth
EOF
    fi

    success "Queue filled to depth $new_depth"

    # Log event
    if [ -f "$EVENTS_FILE" ]; then
        cat >> "$EVENTS_FILE" << EOF

- timestamp: "$timestamp"
  type: queue_refilled
  agent: planner
  run_id: "$RUN_ID"
  data:
    previous_depth: $current_depth
    new_depth: $new_depth
    tasks_added: $added
EOF
    fi
}

# Main
case "${1:---fill}" in
    --check)
        depth=$(check_queue_depth)
        echo "Queue depth: $depth"
        if [ "$depth" -lt "$QUEUE_DEPTH_TARGET_MIN" ]; then
            echo "Status: NEEDS REFILL (target: $QUEUE_DEPTH_TARGET_MIN-$QUEUE_DEPTH_TARGET_MAX)"
            exit 1
        else
            echo "Status: OK"
            exit 0
        fi
        ;;
    --fill)
        fill_queue
        ;;
    --pending)
        log "Pending tasks (sorted by priority):"
        get_pending_tasks | while read -r line; do
            task_id=$(echo "$line" | cut -d'|' -f1)
            score=$(echo "$line" | cut -d'|' -f2)
            title=$(echo "$line" | cut -d'|' -f3)
            echo "  $task_id (score: $score) - $title"
        done
        ;;
    *)
        echo "Usage: $0 [--check | --fill | --pending]"
        echo "  --check   - Check if queue needs refill"
        echo "  --fill    - Fill queue to target depth (default)"
        echo "  --pending - List pending tasks sorted by priority"
        exit 1
        ;;
esac
