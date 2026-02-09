#!/bin/bash
# BB5 Parallel Task Dispatch Script
# Coordinates with queue manager to dispatch tasks to available execution slots
#
# Usage: bb5-parallel-dispatch.sh [--dry-run] [--monitor] [--force]

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
RUN_ID="${RALF_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"

# Paths
CONFIG_DIR="$PROJECT_ROOT/.autonomous/config"
EXECUTION_STATE="$CONFIG_DIR/execution-state.yaml"
QUEUE_FILE="$PROJECT_ROOT/.autonomous/agents/communications/queue.yaml"
TASKS_DIR="$PROJECT_ROOT/tasks/active"
LOGS_DIR="$PROJECT_ROOT/.autonomous/logs/dispatch"
PID_DIR="$PROJECT_ROOT/.autonomous/run"

# Slot configuration
MAX_SLOTS=5
SLOT_PREFIX="slot"

# Heartbeat settings
HEARTBEAT_INTERVAL=30
HEARTBEAT_TIMEOUT=120

# Lock file paths
EXECUTION_STATE_LOCK="$CONFIG_DIR/.execution-state.lock"
QUEUE_LOCK="$PROJECT_ROOT/.autonomous/agents/communications/.queue.lock"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Logging
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [DISPATCH] $1"
    echo -e "${BLUE}$msg${NC}"
    echo "$msg" >> "$LOGS_DIR/dispatch-$(date +%Y%m%d).log" 2>/dev/null || true
}

log_info() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [DISPATCH] $1"
    echo -e "${CYAN}$msg${NC}"
    echo "$msg" >> "$LOGS_DIR/dispatch-$(date +%Y%m%d).log" 2>/dev/null || true
}

log_success() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [DISPATCH] $1"
    echo -e "${GREEN}$msg${NC}"
    echo "$msg" >> "$LOGS_DIR/dispatch-$(date +%Y%m%d).log" 2>/dev/null || true
}

log_warning() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [DISPATCH] $1"
    echo -e "${YELLOW}$msg${NC}"
    echo "$msg" >> "$LOGS_DIR/dispatch-$(date +%Y%m%d).log" 2>/dev/null || true
}

log_error() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [DISPATCH] $1"
    echo -e "${RED}$msg${NC}"
    echo "$msg" >> "$LOGS_DIR/dispatch-$(date +%Y%m%d).log" 2>/dev/null || true
}

# Initialize directories and state
init() {
    mkdir -p "$CONFIG_DIR" "$LOGS_DIR" "$PID_DIR"

    # Create execution state if it doesn't exist
    if [ ! -f "$EXECUTION_STATE" ]; then
        cat > "$EXECUTION_STATE" << EOF
execution_state:
  version: "1.0"
  last_updated: "$(date -Iseconds)"
  dispatch_id: "$RUN_ID"

slots:
  slot_1:
    id: 1
    status: available
    profile: general
    current_task: null
    started_at: null
    heartbeat_at: null
    pid: null
  slot_2:
    id: 2
    status: available
    profile: compute
    current_task: null
    started_at: null
    heartbeat_at: null
    pid: null
  slot_3:
    id: 3
    status: available
    profile: io
    current_task: null
    started_at: null
    heartbeat_at: null
    pid: null
  slot_4:
    id: 4
    status: available
    profile: memory
    current_task: null
    started_at: null
    heartbeat_at: null
    pid: null
  slot_5:
    id: 5
    status: available
    profile: general
    current_task: null
    started_at: null
    heartbeat_at: null
    pid: null

metrics:
  tasks_dispatched: 0
  tasks_completed: 0
  tasks_failed: 0
  tasks_preempted: 0
  last_dispatch: null
  last_completion: null
EOF
        log "Initialized execution state with $MAX_SLOTS slots"
    fi
}

# Get slot status
get_slot_status() {
    local slot_id="$1"
    yq eval ".slots.${SLOT_PREFIX}_${slot_id}.status" "$EXECUTION_STATE" 2>/dev/null || echo "unknown"
}

# Get slot profile
get_slot_profile() {
    local slot_id="$1"
    yq eval ".slots.${SLOT_PREFIX}_${slot_id}.profile" "$EXECUTION_STATE" 2>/dev/null || echo "general"
}

# Get current task for slot
get_slot_task() {
    local slot_id="$1"
    yq eval ".slots.${SLOT_PREFIX}_${slot_id}.current_task" "$EXECUTION_STATE" 2>/dev/null || echo "null"
}

# Update slot in execution state
update_slot() {
    local slot_id="$1"
    local field="$2"
    local value="$3"

    # Ensure lock directory exists
    mkdir -p "$(dirname "$EXECUTION_STATE_LOCK")"

    # Lock execution state for modification
    (
        flock -x 200 || exit 1
        if [ "$value" = "null" ] || [ "$value" = "true" ] || [ "$value" = "false" ]; then
            yq eval -i ".slots.${SLOT_PREFIX}_${slot_id}.${field} = ${value}" "$EXECUTION_STATE"
        else
            yq eval -i ".slots.${SLOT_PREFIX}_${slot_id}.${field} = \"$value\"" "$EXECUTION_STATE"
        fi

        # Update last_updated timestamp
        yq eval -i ".execution_state.last_updated = \"$(date -Iseconds)\"" "$EXECUTION_STATE"
    ) 200>"$EXECUTION_STATE_LOCK"
}

# Get available slots
get_available_slots() {
    local available=""
    for i in $(seq 1 $MAX_SLOTS); do
        local status=$(get_slot_status "$i")
        if [ "$status" = "available" ]; then
            available="$available $i"
        fi
    done
    echo "$available" | xargs
}

# Count available slots
count_available_slots() {
    get_available_slots | wc -w | tr -d ' '
}

# Get ready tasks from queue (status = pending, not claimed)
get_ready_tasks() {
    if [ ! -f "$QUEUE_FILE" ]; then
        log_warning "Queue file not found: $QUEUE_FILE"
        return
    fi

    # Extract pending tasks that aren't claimed
    yq eval '.queue[] | select(.status == "pending") | select(.claimed_by == null) | .task_id' "$QUEUE_FILE" 2>/dev/null | head -20
}

# Get task details from queue
get_task_details() {
    local task_id="$1"

    if [ ! -f "$QUEUE_FILE" ]; then
        echo "null"
        return
    fi

    # Find task in queue and extract details
    yq eval ".queue[] | select(.task_id == \"$task_id\")" "$QUEUE_FILE" 2>/dev/null
}

# Get task resource type (from task file or infer from task)
get_task_resource_type() {
    local task_id="$1"
    local task_file="$TASKS_DIR/$task_id/task.md"

    if [ -f "$task_file" ]; then
        # Check for resource_type in task metadata
        local resource_type=$(grep -i "resource_type:" "$task_file" | head -1 | cut -d':' -f2 | tr -d ' ' || echo "")
        if [ -n "$resource_type" ]; then
            echo "$resource_type"
            return
        fi

        # Infer from task content
        if grep -qi "database\|sql\|migration\|schema" "$task_file"; then
            echo "io"
        elif grep -qi "compute\|algorithm\|processing\|analysis" "$task_file"; then
            echo "compute"
        elif grep -qi "memory\|cache\|storage" "$task_file"; then
            echo "memory"
        else
            echo "general"
        fi
    else
        echo "general"
    fi
}

# Match task to best slot
match_task_to_slot() {
    local task_id="$1"
    local available_slots="$2"

    local task_resource=$(get_task_resource_type "$task_id")
    local best_slot=""
    local best_match_score=0

    for slot_id in $available_slots; do
        local slot_profile=$(get_slot_profile "$slot_id")
        local match_score=0

        # Score matching
        if [ "$task_resource" = "$slot_profile" ]; then
            match_score=100  # Perfect match
        elif [ "$slot_profile" = "general" ]; then
            match_score=50   # General can handle anything
        elif [ "$task_resource" = "general" ]; then
            match_score=50   # General task can go anywhere
        else
            match_score=10   # Mismatch but usable
        fi

        if [ $match_score -gt $best_match_score ]; then
            best_match_score=$match_score
            best_slot=$slot_id
        fi
    done

    echo "$best_slot"
}

# Claim task in queue
claim_task() {
    local task_id="$1"
    local slot_id="$2"

    if [ ! -f "$QUEUE_FILE" ]; then
        return 1
    fi

    local claim_id="${RUN_ID}-slot${slot_id}"
    local timestamp=$(date -Iseconds)

    # Ensure lock directory exists
    mkdir -p "$(dirname "$QUEUE_LOCK")"

    # Lock queue file for modification
    (
        flock -x 200 || exit 1
        yq eval -i "(.queue[] | select(.task_id == \"$task_id\")).claimed_by = \"$claim_id\"" "$QUEUE_FILE"
        yq eval -i "(.queue[] | select(.task_id == \"$task_id\")).claimed_at = \"$timestamp\"" "$QUEUE_FILE"
    ) 200>"$QUEUE_LOCK"

    log_info "Claimed task $task_id for slot $slot_id (claim: $claim_id)"
    return 0
}

# Update task status in queue
update_task_status() {
    local task_id="$1"
    local status="$2"
    local notes="${3:-}"

    if [ ! -f "$QUEUE_FILE" ]; then
        return 1
    fi

    local timestamp=$(date -Iseconds)

    # Ensure lock directory exists
    mkdir -p "$(dirname "$QUEUE_LOCK")"

    # Lock queue file for modification
    (
        flock -x 200 || exit 1
        yq eval -i "(.queue[] | select(.task_id == \"$task_id\")).status = \"$status\"" "$QUEUE_FILE"

        if [ "$status" = "in_progress" ]; then
            yq eval -i "(.queue[] | select(.task_id == \"$task_id\")).started_at = \"$timestamp\"" "$QUEUE_FILE"
        elif [ "$status" = "completed" ] || [ "$status" = "failed" ]; then
            yq eval -i "(.queue[] | select(.task_id == \"$task_id\")).completed_at = \"$timestamp\"" "$QUEUE_FILE"
        fi

        if [ -n "$notes" ]; then
            yq eval -i "(.queue[] | select(.task_id == \"$task_id\")).notes += \" | $notes\"" "$QUEUE_FILE"
        fi
    ) 200>"$QUEUE_LOCK"
}

# Launch task in slot
launch_task() {
    local task_id="$1"
    local slot_id="$2"

    local task_file="$TASKS_DIR/$task_id/task.md"
    if [ ! -f "$task_file" ]; then
        log_error "Task file not found: $task_file"
        return 1
    fi

    local timestamp=$(date -Iseconds)
    local pid_file="$PID_DIR/slot-${slot_id}.pid"
    local slot_log="$LOGS_DIR/slot-${slot_id}-$(date +%Y%m%d-%H%M%S).log"

    # Update slot state
    update_slot "$slot_id" "status" "busy"
    update_slot "$slot_id" "current_task" "$task_id"
    update_slot "$slot_id" "started_at" "$timestamp"
    update_slot "$slot_id" "heartbeat_at" "$timestamp"

    # Create task execution wrapper
    local wrapper_script="$PID_DIR/slot-${slot_id}-wrapper.sh"
    cat > "$wrapper_script" << EOF
#!/bin/bash
# Auto-generated task wrapper for slot $slot_id, task $task_id

# Update heartbeat function
update_heartbeat() {
    yq eval -i ".slots.${SLOT_PREFIX}_${slot_id}.heartbeat_at = \"\$(date -Iseconds)\"" "$EXECUTION_STATE"
}

# Signal completion
signal_completion() {
    local exit_code=\$1
    local result_file="$PID_DIR/slot-${slot_id}-result"
    echo "exit_code=\$exit_code" > "\$result_file"
    echo "completed_at=\$(date -Iseconds)" >> "\$result_file"
}

# Heartbeat loop in background
(
    while true; do
        update_heartbeat
        sleep $HEARTBEAT_INTERVAL
    done
) &
HEARTBEAT_PID=\$!

# Execute task
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting task $task_id in slot $slot_id"

# Source RALF loop for task execution
export RALF_PROJECT_ROOT="$PROJECT_ROOT"
export RALF_TASK_ID="$task_id"
export RALF_SLOT_ID="$slot_id"
export RALF_RUN_ID="$RUN_ID"

# Run the task via ralf-loop.sh
cd "$PROJECT_ROOT"
if "$SCRIPT_DIR/../../../2-engine/.autonomous/shell/ralf-loop.sh" --task "$task_id" >> "$slot_log" 2>&1; then
    signal_completion 0
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task $task_id completed successfully"
else
    signal_completion \$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task $task_id failed with exit code \$?"
fi

# Cleanup
kill \$HEARTBEAT_PID 2>/dev/null || true
rm -f "$pid_file" "$wrapper_script"
EOF

    chmod +x "$wrapper_script"

    # Launch in background
    (
        exec "$wrapper_script"
    ) &
    local pid=$!

    # Record PID
    echo $pid > "$pid_file"
    update_slot "$slot_id" "pid" "$pid"

    # Update task status
    update_task_status "$task_id" "in_progress"

    # Update metrics (with lock)
    (
        flock -x 200 || exit 1
        yq eval -i ".metrics.tasks_dispatched = (.metrics.tasks_dispatched // 0) + 1" "$EXECUTION_STATE"
        yq eval -i ".metrics.last_dispatch = \"$timestamp\"" "$EXECUTION_STATE"
    ) 200>"$EXECUTION_STATE_LOCK"

    log_success "Launched task $task_id in slot $slot_id (PID: $pid)"
    return 0
}

# Check if slot is still alive
check_slot_alive() {
    local slot_id="$1"
    local pid_file="$PID_DIR/slot-${slot_id}.pid"

    if [ ! -f "$pid_file" ]; then
        return 1
    fi

    local pid=$(cat "$pid_file" 2>/dev/null)
    if [ -z "$pid" ]; then
        return 1
    fi

    # Check if process exists
    if kill -0 "$pid" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Check slot heartbeat
check_slot_heartbeat() {
    local slot_id="$1"
    local heartbeat=$(yq eval ".slots.${SLOT_PREFIX}_${slot_id}.heartbeat_at" "$EXECUTION_STATE" 2>/dev/null)

    if [ "$heartbeat" = "null" ] || [ -z "$heartbeat" ]; then
        return 1
    fi

    # Convert to epoch seconds
    local heartbeat_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${heartbeat%%.*}" +%s 2>/dev/null || date -d "$heartbeat" +%s 2>/dev/null)
    local now_epoch=$(date +%s)
    local diff=$((now_epoch - heartbeat_epoch))

    if [ $diff -gt $HEARTBEAT_TIMEOUT ]; then
        return 1  # Stale heartbeat
    fi

    return 0
}

# Handle slot completion or failure
finalize_slot() {
    local slot_id="$1"
    local status="$2"  # completed or failed

    local task_id=$(get_slot_task "$slot_id")
    local timestamp=$(date -Iseconds)

    # Update task status
    if [ "$task_id" != "null" ] && [ -n "$task_id" ]; then
        update_task_status "$task_id" "$status" "Executed in slot $slot_id"
    fi

    # Reset slot
    update_slot "$slot_id" "status" "available"
    update_slot "$slot_id" "current_task" "null"
    update_slot "$slot_id" "started_at" "null"
    update_slot "$slot_id" "heartbeat_at" "null"
    update_slot "$slot_id" "pid" "null"

    # Update metrics (with lock)
    (
        flock -x 200 || exit 1
        if [ "$status" = "completed" ]; then
            yq eval -i ".metrics.tasks_completed = (.metrics.tasks_completed // 0) + 1" "$EXECUTION_STATE"
        else
            yq eval -i ".metrics.tasks_failed = (.metrics.tasks_failed // 0) + 1" "$EXECUTION_STATE"
        fi
        yq eval -i ".metrics.last_completion = \"$timestamp\"" "$EXECUTION_STATE"
    ) 200>"$EXECUTION_STATE_LOCK"

    log_info "Slot $slot_id finalized (task $task_id: $status)"
}

# Monitor running slots
monitor_slots() {
    for slot_id in $(seq 1 $MAX_SLOTS); do
        local status=$(get_slot_status "$slot_id")

        if [ "$status" = "busy" ]; then
            # Check if process is still running
            if ! check_slot_alive "$slot_id"; then
                # Process died, check for result
                local result_file="$PID_DIR/slot-${slot_id}-result"
                if [ -f "$result_file" ]; then
                    local exit_code=$(grep "exit_code=" "$result_file" | cut -d'=' -f2)
                    if [ "$exit_code" = "0" ]; then
                        finalize_slot "$slot_id" "completed"
                    else
                        finalize_slot "$slot_id" "failed"
                    fi
                    rm -f "$result_file"
                else
                    # No result file, assume failure
                    finalize_slot "$slot_id" "failed"
                fi
            else
                # Process running, check heartbeat
                if ! check_slot_heartbeat "$slot_id"; then
                    log_warning "Slot $slot_id has stale heartbeat"
                    # Optionally kill and restart
                fi
            fi
        fi
    done
}

# Preempt slot for critical task
preempt_slot() {
    local slot_id="$1"
    local new_task_id="$2"

    local current_task=$(get_slot_task "$slot_id")
    local pid_file="$PID_DIR/slot-${slot_id}.pid"

    log_warning "Preempting slot $slot_id (task: $current_task) for critical task $new_task_id"

    # Kill current process
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file" 2>/dev/null)
        if [ -n "$pid" ]; then
            kill -TERM "$pid" 2>/dev/null || true
            sleep 2
            kill -KILL "$pid" 2>/dev/null || true
        fi
    fi

    # Update preempted task status
    if [ "$current_task" != "null" ] && [ -n "$current_task" ]; then
        update_task_status "$current_task" "pending" "Preempted for $new_task_id"
        # Remove claim (with lock)
        (
            flock -x 200 || exit 1
            yq eval -i "(.queue[] | select(.task_id == \"$current_task\")).claimed_by = null" "$QUEUE_FILE"
            yq eval -i "(.queue[] | select(.task_id == \"$current_task\")).claimed_at = null" "$QUEUE_FILE"
        ) 200>"$QUEUE_LOCK"
    fi

    # Update metrics (with lock)
    (
        flock -x 200 || exit 1
        yq eval -i ".metrics.tasks_preempted = (.metrics.tasks_preempted // 0) + 1" "$EXECUTION_STATE"
    ) 200>"$EXECUTION_STATE_LOCK"

    # Reset slot
    update_slot "$slot_id" "status" "available"
    update_slot "$slot_id" "current_task" "null"
    update_slot "$slot_id" "started_at" "null"
    update_slot "$slot_id" "heartbeat_at" "null"
    update_slot "$slot_id" "pid" "null"

    log_success "Slot $slot_id preempted and ready for $new_task_id"
}

# Check for critical tasks that need immediate execution
check_critical_tasks() {
    if [ ! -f "$QUEUE_FILE" ]; then
        return
    fi

    # Find critical priority tasks
    local critical_tasks=$(yq eval '.queue[] | select(.priority == "critical") | select(.status == "pending") | .task_id' "$QUEUE_FILE" 2>/dev/null)

    for task_id in $critical_tasks; do
        # Check if already assigned
        local claimed=$(yq eval ".queue[] | select(.task_id == \"$task_id\") | .claimed_by" "$QUEUE_FILE" 2>/dev/null)
        if [ "$claimed" != "null" ] && [ -n "$claimed" ]; then
            continue
        fi

        # Try to find available slot
        local available=$(get_available_slots)
        if [ -n "$available" ]; then
            local best_slot=$(match_task_to_slot "$task_id" "$available")
            if [ -n "$best_slot" ]; then
                claim_task "$task_id" "$best_slot"
                launch_task "$task_id" "$best_slot"
                continue
            fi
        fi

        # No available slots - check for preemption
        # Find lowest priority running task
        local lowest_priority_slot=""
        local lowest_priority_score=999

        for slot_id in $(seq 1 $MAX_SLOTS); do
            local slot_status=$(get_slot_status "$slot_id")
            if [ "$slot_status" = "busy" ]; then
                local slot_task=$(get_slot_task "$slot_id")
                local task_priority=$(yq eval ".queue[] | select(.task_id == \"$slot_task\") | .priority" "$QUEUE_FILE" 2>/dev/null)
                local priority_score=5
                case "$task_priority" in
                    critical) priority_score=1 ;;
                    high) priority_score=3 ;;
                    medium) priority_score=5 ;;
                    low) priority_score=7 ;;
                esac

                if [ $priority_score -gt $lowest_priority_score ]; then
                    lowest_priority_score=$priority_score
                    lowest_priority_slot=$slot_id
                fi
            fi
        done

        # Preempt if found
        if [ -n "$lowest_priority_slot" ]; then
            preempt_slot "$lowest_priority_slot" "$task_id"
            claim_task "$task_id" "$lowest_priority_slot"
            launch_task "$task_id" "$lowest_priority_slot"
        fi
    done
}

# Main dispatch loop
dispatch_loop() {
    log "Starting parallel dispatch loop (Run ID: $RUN_ID)"
    log "Max slots: $MAX_SLOTS | Heartbeat: ${HEARTBEAT_INTERVAL}s | Timeout: ${HEARTBEAT_TIMEOUT}s"

    local dry_run=false
    local monitor_only=false
    local force_dispatch=false

    # Parse arguments
    for arg in "$@"; do
        case "$arg" in
            --dry-run)
                dry_run=true
                log "DRY RUN MODE - No actual execution"
                ;;
            --monitor)
                monitor_only=true
                log "MONITOR MODE - Only monitoring, no dispatch"
                ;;
            --force)
                force_dispatch=true
                log "FORCE MODE - Will dispatch even if queue depth low"
                ;;
        esac
    done

    # Main loop
    while true; do
        # Monitor existing slots
        monitor_slots

        if [ "$monitor_only" = false ]; then
            # Check for critical tasks first
            check_critical_tasks

            # Get available slots
            local available_count=$(count_available_slots)

            if [ "$available_count" -gt 0 ]; then
                log_info "Available slots: $available_count"

                # Get ready tasks
                local ready_tasks=$(get_ready_tasks)
                local ready_count=$(echo "$ready_tasks" | grep -c "^TASK-" || echo "0")

                if [ "$ready_count" -gt 0 ]; then
                    log "Ready tasks: $ready_count"

                    # Match and dispatch tasks
                    local available=$(get_available_slots)
                    local dispatched=0

                    for task_id in $ready_tasks; do
                        if [ "$dispatched" -ge "$available_count" ]; then
                            break
                        fi

                        # Check if task already claimed
                        local claimed=$(yq eval ".queue[] | select(.task_id == \"$task_id\") | .claimed_by" "$QUEUE_FILE" 2>/dev/null)
                        if [ "$claimed" != "null" ] && [ -n "$claimed" ]; then
                            continue
                        fi

                        # Find best slot
                        local remaining_available=$(get_available_slots)
                        if [ -z "$remaining_available" ]; then
                            break
                        fi

                        local best_slot=$(match_task_to_slot "$task_id" "$remaining_available")

                        if [ -n "$best_slot" ]; then
                            if [ "$dry_run" = true ]; then
                                log "[DRY RUN] Would dispatch $task_id to slot $best_slot"
                            else
                                if claim_task "$task_id" "$best_slot"; then
                                    if launch_task "$task_id" "$best_slot"; then
                                        dispatched=$((dispatched + 1))
                                    fi
                                fi
                            fi
                        fi
                    done

                    if [ "$dispatched" -gt 0 ]; then
                        log_success "Dispatched $dispatched task(s)"
                    fi
                else
                    log "No ready tasks in queue"
                fi
            fi
        fi

        # Print status summary
        local busy_count=0
        for i in $(seq 1 $MAX_SLOTS); do
            local s=$(get_slot_status "$i")
            if [ "$s" = "busy" ]; then
                busy_count=$((busy_count + 1))
            fi
        done

        log_info "Status: $busy_count/$MAX_SLOTS busy, $available_count/$MAX_SLOTS available"

        # Sleep before next iteration
        sleep 5
    done
}

# Show current status
show_status() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           BB5 Parallel Dispatch Status                     ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    if [ ! -f "$EXECUTION_STATE" ]; then
        echo "Execution state not initialized. Run with --start first."
        return 1
    fi

    echo "Last Updated: $(yq eval '.execution_state.last_updated' "$EXECUTION_STATE")"
    echo "Dispatch ID:  $(yq eval '.execution_state.dispatch_id' "$EXECUTION_STATE")"
    echo ""

    echo "Execution Slots:"
    echo "┌──────┬────────────┬───────────┬─────────────────┬─────────────────────────┐"
    echo "│ Slot │ Profile    │ Status    │ Current Task    │ Started                 │"
    echo "├──────┼────────────┼───────────┼─────────────────┼─────────────────────────┤"

    for i in $(seq 1 $MAX_SLOTS); do
        local profile=$(get_slot_profile "$i")
        local status=$(get_slot_status "$i")
        local task=$(get_slot_task "$i")
        local started=$(yq eval ".slots.${SLOT_PREFIX}_${i}.started_at" "$EXECUTION_STATE")

        if [ "$task" = "null" ]; then
            task="-"
        fi

        if [ "$started" = "null" ] || [ -z "$started" ]; then
            started="-"
        else
            started="${started:0:19}"
        fi

        printf "│ %4s │ %-10s │ %-9s │ %-15s │ %-23s │\n" "$i" "$profile" "$status" "${task:0:15}" "$started"
    done

    echo "└──────┴────────────┴───────────┴─────────────────┴─────────────────────────┘"
    echo ""

    echo "Metrics:"
    yq eval '.metrics' "$EXECUTION_STATE"
    echo ""

    echo "Recent Log Entries:"
    if [ -f "$LOGS_DIR/dispatch-$(date +%Y%m%d).log" ]; then
        tail -10 "$LOGS_DIR/dispatch-$(date +%Y%m%d).log"
    else
        echo "No log entries for today"
    fi
    echo ""
}

# Cleanup all slots
cleanup() {
    log "Cleaning up dispatch system..."

    for slot_id in $(seq 1 $MAX_SLOTS); do
        local pid_file="$PID_DIR/slot-${slot_id}.pid"
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file" 2>/dev/null)
            if [ -n "$pid" ]; then
                kill -TERM "$pid" 2>/dev/null || true
                sleep 1
                kill -KILL "$pid" 2>/dev/null || true
            fi
            rm -f "$pid_file"
        fi

        # Reset slot state
        update_slot "$slot_id" "status" "available"
        update_slot "$slot_id" "current_task" "null"
        update_slot "$slot_id" "started_at" "null"
        update_slot "$slot_id" "heartbeat_at" "null"
        update_slot "$slot_id" "pid" "null"
    done

    # Clean up wrapper scripts
    rm -f "$PID_DIR"/slot-*-wrapper.sh
    rm -f "$PID_DIR"/slot-*-result

    log_success "Cleanup complete"
}

# Main entry point
main() {
    case "${1:-status}" in
        --start|-s)
            init
            shift
            dispatch_loop "$@"
            ;;
        --status|-st)
            show_status
            ;;
        --stop|--cleanup)
            cleanup
            ;;
        --monitor|-m)
            init
            dispatch_loop --monitor
            ;;
        --dry-run|-d)
            init
            dispatch_loop --dry-run
            ;;
        --help|-h)
            cat << EOF
BB5 Parallel Task Dispatch Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  --start, -s       Start the dispatch loop (default)
  --status, -st     Show current execution status
  --stop, --cleanup Stop all slots and cleanup
  --monitor, -m     Monitor mode only (no dispatch)
  --dry-run, -d     Dry run mode (no actual execution)
  --help, -h        Show this help message

Options (for --start):
  --force           Force dispatch even with low queue depth

Examples:
  $0 --start                    # Start dispatch loop
  $0 --start --force            # Start with force dispatch
  $0 --status                   # Show current status
  $0 --stop                     # Stop and cleanup

Configuration:
  Max Slots:        $MAX_SLOTS
  Heartbeat:        ${HEARTBEAT_INTERVAL}s
  Timeout:          ${HEARTBEAT_TIMEOUT}s
  Execution State:  $EXECUTION_STATE
  Queue File:       $QUEUE_FILE
EOF
            ;;
        *)
            echo "Unknown command: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
}

# Handle signals
trap 'log "Received interrupt signal, shutting down..."; cleanup; exit 0' INT TERM

# Run main
main "$@"
