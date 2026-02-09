#!/bin/bash
# RALF Planner Queue Automation
# Automatically populates queue.yaml with prioritized tasks
# Now uses StorageBackend (SQLite with YAML fallback)
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

# Source libraries
source "${SCRIPT_DIR}/../../2-engine/helpers/legacy/paths.sh"
source "${SCRIPT_DIR}/../../2-engine/helpers/legacy/error_handler.sh"

# Paths
PROJECT_MEMORY="$(get_project_path)"
TASKS_DIR="$PROJECT_MEMORY/tasks/active"
QUEUE_FILE="$(get_project_path)/.autonomous/agents/communications/queue.yaml"
EVENTS_FILE="$PROJECT_MEMORY/.autonomous/agents/communications/events.yaml"
STORAGE_BACKEND="$PROJECT_MEMORY/.autonomous/lib/storage_backend.py"

# Ensure communications directory exists
COMMUNICATIONS_DIR="$(get_project_path)/.autonomous/agents/communications"
if ! eh_dir_exists "$COMMUNICATIONS_DIR" "communications"; then
    eh_ensure_dir "$COMMUNICATIONS_DIR" || {
        warning "Cannot create communications directory"
    }
fi

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

# Check if storage backend exists
if ! eh_file_exists "$STORAGE_BACKEND" "storage backend check"; then
    warning "Storage backend not found: $STORAGE_BACKEND"
    warning "Falling back to YAML-only mode"
    USE_STORAGE_BACKEND=false
else
    USE_STORAGE_BACKEND=true
fi

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
    if [ "$USE_STORAGE_BACKEND" = true ]; then
        # Use storage backend to count pending tasks
        python3 "$STORAGE_BACKEND" stats 2>/dev/null | grep "^status:pending:" | cut -d: -f3
    else
        # Fallback to YAML parsing
        if ! eh_file_exists "$QUEUE_FILE" "queue depth check"; then
            log "Queue file not found, creating minimal queue"
            eh_create_minimal_queue "$QUEUE_FILE"
            echo "0"
            return
        fi
        awk '/^  - task_id:/{task=1} /^    status: pending/{pending++} END{print pending+0}' "$QUEUE_FILE"
    fi
}

# Get pending tasks from tasks/active/
get_pending_tasks() {
    local pending_tasks=""

    # Check if tasks directory exists
    if ! eh_dir_exists "$TASKS_DIR" "tasks directory"; then
        warning "Tasks directory not found: $TASKS_DIR"
        echo ""
        return
    fi

    for task_dir in "$TASKS_DIR"/TASK-*; do
        [ -d "$task_dir" ] || continue

        local task_file="$task_dir/task.md"
        if ! eh_file_exists "$task_file" "task file check"; then
            continue
        fi

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

    if [ "$USE_STORAGE_BACKEND" = true ]; then
        # Add to SQLite via storage backend
        python3 "$STORAGE_BACKEND" add-task \
            --task-id "$task_id" \
            --title "$title" \
            --priority "$priority" \
            --score "$score" \
            --minutes "$estimated_minutes" \
            --lines "$lines" 2>/dev/null || true
    fi

    # Ensure queue file exists
    if ! eh_file_exists "$QUEUE_FILE" "queue append"; then
        eh_create_minimal_queue "$QUEUE_FILE"
    fi

    # Also append to queue.yaml for compatibility
    (
        flock -x 200
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
    ) 200>"$PROJECT_MEMORY/.autonomous/agents/communications/.queue.lock"

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

    # Ensure queue file exists before updating metadata
    if ! eh_file_exists "$QUEUE_FILE" "metadata update"; then
        eh_create_minimal_queue "$QUEUE_FILE"
    fi

    # Update or add metadata section (with file locking)
    (
        flock -x 200
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
    ) 200>"$PROJECT_MEMORY/.autonomous/agents/communications/.queue.lock"

    success "Queue filled to depth $new_depth"

    # Log event with file locking
    if eh_file_exists "$EVENTS_FILE" "event logging"; then
        (
            flock -x 200
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
        ) 200>"$PROJECT_MEMORY/.autonomous/agents/communications/.events.lock"
    else
        warning "events.yaml not found - event not logged"
    fi
}

# Sync SQLite to YAML (for backup/compatibility)
sync_to_yaml() {
    if [ "$USE_STORAGE_BACKEND" = true ]; then
        log "Syncing SQLite to YAML..."
        python3 "$STORAGE_BACKEND" sync 2>/dev/null || warning "Sync failed"
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
        sync_to_yaml
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
    --sync)
        sync_to_yaml
        ;;
    *)
        echo "Usage: $0 [--check | --fill | --pending | --sync]"
        echo "  --check   - Check if queue needs refill"
        echo "  --fill    - Fill queue to target depth (default)"
        echo "  --pending - List pending tasks sorted by priority"
        echo "  --sync    - Sync SQLite data to YAML"
        exit 1
        ;;
esac
