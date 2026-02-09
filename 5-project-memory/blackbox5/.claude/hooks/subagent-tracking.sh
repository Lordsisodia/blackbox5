#!/bin/bash
# subagent-tracking.sh - Smart subagent start/stop tracking for BB5
# Purpose: Track agent lifecycle without environment variables
# Usage: Called with "start" or "stop" argument

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BB5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"
COMM_DIR="$BB5_DIR/.autonomous/agents/communications"

EVENT_TYPE="${1:-start}"  # "start" or "stop"

# =============================================================================
# CONTEXT PERSISTENCE
# =============================================================================

# File to persist agent context between start and stop
CONTEXT_FILE="$BB5_DIR/.agent-context"

save_context() {
    local agent_type="$1"
    local agent_id="$2"
    local parent_task="$3"
    local run_id="$4"
    local timestamp=$(date -Iseconds)

    # Determine agent_type from .ralf-metadata if available
    local detected_agent_type="$agent_type"
    if [ -n "$run_id" ]; then
        local run_dir=""
        # Try to find the run directory
        if [ -d "$BB5_DIR/runs/unknown/$run_id" ]; then
            run_dir="$BB5_DIR/runs/unknown/$run_id"
        elif [ -d "$BB5_DIR/runs/planner/$run_id" ]; then
            run_dir="$BB5_DIR/runs/planner/$run_id"
        elif [ -d "$BB5_DIR/runs/executor/$run_id" ]; then
            run_dir="$BB5_DIR/runs/executor/$run_id"
        elif [ -d "$BB5_DIR/runs/architect/$run_id" ]; then
            run_dir="$BB5_DIR/runs/architect/$run_id"
        fi

        # Read agent_type from .ralf-metadata if available
        if [ -n "$run_dir" ] && [ -f "$run_dir/.ralf-metadata" ]; then
            local meta_agent_type=$(grep "agent_type:" "$run_dir/.ralf-metadata" | head -1 | cut -d':' -f2 | tr -d ' "' || echo "")
            if [ -n "$meta_agent_type" ] && [ "$meta_agent_type" != "unknown" ]; then
                detected_agent_type="$meta_agent_type"
            fi
        fi
    fi

    # Query queue.yaml for parent_task if not already set and we have an agent_type
    local detected_parent_task="$parent_task"
    if [ -z "$detected_parent_task" ] && [ -f "$COMM_DIR/queue.yaml" ]; then
        # Look for claimed_by matching our agent_type and extract task_id
        detected_parent_task=$(grep -B10 "claimed_by:.*$detected_agent_type" "$COMM_DIR/queue.yaml" 2>/dev/null | grep "task_id:" | tail -1 | cut -d':' -f2 | tr -d ' "' || echo "")
    fi

    # Construct full agent_id
    local full_agent_id="${detected_agent_type}-${run_id:-$(date +%s)}"
    if [ -n "$run_id" ]; then
        full_agent_id="${detected_agent_type}-${run_id}"
    fi

    # Save context to file
    cat > "$CONTEXT_FILE" << EOF
# Agent Context - Auto-generated
# DO NOT EDIT - This file is managed by subagent-tracking.sh
agent_type: "$detected_agent_type"
agent_id: "$full_agent_id"
parent_task: "$detected_parent_task"
run_id: "$run_id"
timestamp: "$timestamp"
EOF

    echo "Context saved: $detected_agent_type | $full_agent_id | $detected_parent_task"
}

load_context() {
    local agent_type="unknown"
    local agent_id="unknown"
    local parent_task=""
    local run_id=""
    local timestamp=$(date -Iseconds)

    # Load from persisted context file if it exists
    if [ -f "$CONTEXT_FILE" ]; then
        agent_type=$(grep "agent_type:" "$CONTEXT_FILE" | cut -d':' -f2 | tr -d ' "' || echo "unknown")
        agent_id=$(grep "agent_id:" "$CONTEXT_FILE" | cut -d':' -f2 | tr -d ' "' || echo "unknown")
        parent_task=$(grep "parent_task:" "$CONTEXT_FILE" | cut -d':' -f2 | tr -d ' "' || echo "")
        run_id=$(grep "run_id:" "$CONTEXT_FILE" | cut -d':' -f2 | tr -d ' "' || echo "")
        timestamp=$(grep "timestamp:" "$CONTEXT_FILE" | cut -d':' -f2- | tr -d ' "' || echo "$timestamp")
        echo "Loaded persisted context" >&2
    fi

    # Fallback to AGENT_CONTEXT.md if values are still unknown
    if [ "$agent_type" = "unknown" ] && [ -f "$BB5_DIR/AGENT_CONTEXT.md" ]; then
        local ctx_agent_type=$(grep "Detected Agent Type:" "$BB5_DIR/AGENT_CONTEXT.md" | cut -d':' -f2 | tr -d ' *' || echo "")
        if [ -n "$ctx_agent_type" ]; then
            agent_type="$ctx_agent_type"
            echo "Loaded agent_type from AGENT_CONTEXT.md" >&2
        fi
    fi

    # Fallback to .ralf-metadata if available
    if [ -n "$run_id" ]; then
        local run_dir=""
        if [ -d "$BB5_DIR/runs/unknown/$run_id" ]; then
            run_dir="$BB5_DIR/runs/unknown/$run_id"
        elif [ -d "$BB5_DIR/runs/planner/$run_id" ]; then
            run_dir="$BB5_DIR/runs/planner/$run_id"
        elif [ -d "$BB5_DIR/runs/executor/$run_id" ]; then
            run_dir="$BB5_DIR/runs/executor/$run_id"
        elif [ -d "$BB5_DIR/runs/architect/$run_id" ]; then
            run_dir="$BB5_DIR/runs/architect/$run_id"
        fi

        if [ -n "$run_dir" ] && [ -f "$run_dir/.ralf-metadata" ]; then
            local meta_agent_type=$(grep "agent_type:" "$run_dir/.ralf-metadata" | head -1 | cut -d':' -f2 | tr -d ' "' || echo "")
            if [ -n "$meta_agent_type" ] && [ "$meta_agent_type" != "unknown" ]; then
                agent_type="$meta_agent_type"
                echo "Loaded agent_type from .ralf-metadata" >&2
            fi

            # Update agent_id with proper format
            if [ "$agent_type" != "unknown" ]; then
                agent_id="${agent_type}-${run_id}"
            fi
        fi
    fi

    # Query queue.yaml for parent_task if still empty
    if [ -z "$parent_task" ] && [ "$agent_type" != "unknown" ] && [ -f "$COMM_DIR/queue.yaml" ]; then
        parent_task=$(grep -B10 "claimed_by:.*$agent_type" "$COMM_DIR/queue.yaml" 2>/dev/null | grep "task_id:" | tail -1 | cut -d':' -f2 | tr -d ' "' || echo "")
        if [ -n "$parent_task" ]; then
            echo "Loaded parent_task from queue.yaml" >&2
        fi
    fi

    echo "$agent_type|$agent_id|$parent_task|$run_id|$timestamp"
}

# =============================================================================
# SELF-DISCOVERY: Detect agent from context
# =============================================================================

detect_agent_info() {
    local cwd="$(pwd)"
    local agent_type="unknown"
    local agent_id="unknown"
    local parent_task=""
    local run_id=""

    # Method 0: Load persisted context if this is a stop event
    if [ "$EVENT_TYPE" = "stop" ] && [ -f "$CONTEXT_FILE" ]; then
        local persisted=$(load_context)
        agent_type=$(echo "$persisted" | cut -d'|' -f1)
        agent_id=$(echo "$persisted" | cut -d'|' -f2)
        parent_task=$(echo "$persisted" | cut -d'|' -f3)
        run_id=$(echo "$persisted" | cut -d'|' -f4)
        echo "Using persisted context for stop event" >&2
    fi

    # Method 1: Check RALF_RUN_ID environment variable
    if [ -n "${RALF_RUN_ID:-}" ]; then
        run_id="${RALF_RUN_ID}"
    fi

    # Method 2: Extract run_id from RALF_RUN_DIR
    if [ -n "${RALF_RUN_DIR:-}" ]; then
        run_id=$(basename "${RALF_RUN_DIR}")
        # Also try to get agent_type from path
        if [[ "${RALF_RUN_DIR}" == *"/planner/"* ]]; then
            agent_type="planner"
        elif [[ "${RALF_RUN_DIR}" == *"/executor/"* ]]; then
            agent_type="executor"
        elif [[ "${RALF_RUN_DIR}" == *"/architect/"* ]]; then
            agent_type="architect"
        fi
    fi

    # Method 3: Run directory path from cwd
    if [[ "$cwd" == *"/planner/"* ]]; then
        agent_type="planner"
        run_id=$(echo "$cwd" | grep -oE 'run-[0-9]{8}-[0-9]{6}' | tail -1 || echo "")
    elif [[ "$cwd" == *"/executor/"* ]]; then
        agent_type="executor"
        run_id=$(echo "$cwd" | grep -oE 'run-[0-9]{8}-[0-9]{6}' | tail -1 || echo "")
        # Try to find claimed task
        if [ -f "$COMM_DIR/queue.yaml" ]; then
            parent_task=$(grep -B10 "claimed_by:.*executor" "$COMM_DIR/queue.yaml" 2>/dev/null | grep "task_id:" | tail -1 | cut -d':' -f2 | tr -d ' "' || echo "")
        fi
    elif [[ "$cwd" == *"/architect/"* ]]; then
        agent_type="architect"
        run_id=$(echo "$cwd" | grep -oE 'run-[0-9]{8}-[0-9]{6}' | tail -1 || echo "")
    elif [[ "$cwd" == *"/runs/unknown/"* ]]; then
        # Extract run_id from unknown runs
        run_id=$(echo "$cwd" | grep -oE 'run-[0-9]{8}-[0-9]{6}' | tail -1 || echo "")
    fi

    # Method 4: Check .ralf-metadata for agent_type
    if [ -n "$run_id" ]; then
        local run_dir=""
        if [ -d "$BB5_DIR/runs/unknown/$run_id" ]; then
            run_dir="$BB5_DIR/runs/unknown/$run_id"
        elif [ -d "$BB5_DIR/runs/planner/$run_id" ]; then
            run_dir="$BB5_DIR/runs/planner/$run_id"
        elif [ -d "$BB5_DIR/runs/executor/$run_id" ]; then
            run_dir="$BB5_DIR/runs/executor/$run_id"
        elif [ -d "$BB5_DIR/runs/architect/$run_id" ]; then
            run_dir="$BB5_DIR/runs/architect/$run_id"
        fi

        if [ -n "$run_dir" ] && [ -f "$run_dir/.ralf-metadata" ]; then
            local meta_agent_type=$(grep "agent_type:" "$run_dir/.ralf-metadata" | head -1 | cut -d':' -f2 | tr -d ' "' || echo "")
            if [ -n "$meta_agent_type" ] && [ "$meta_agent_type" != "unknown" ]; then
                agent_type="$meta_agent_type"
            fi
        fi
    fi

    # Method 5: Check AGENT_CONTEXT.md
    if [ "$agent_type" = "unknown" ] && [ -f "$BB5_DIR/AGENT_CONTEXT.md" ]; then
        local ctx_agent_type=$(grep "Detected Agent Type:" "$BB5_DIR/AGENT_CONTEXT.md" | cut -d':' -f2 | tr -d ' *' || echo "")
        if [ -n "$ctx_agent_type" ]; then
            agent_type="$ctx_agent_type"
        fi
    fi

    # Construct agent_id
    if [ -n "$run_id" ] && [ "$agent_type" != "unknown" ]; then
        agent_id="${agent_type}-${run_id}"
    elif [ -n "$run_id" ]; then
        agent_id="unknown-${run_id}"
    else
        agent_id="${agent_type}-$(date +%s)"
    fi

    # Query queue.yaml for parent_task if not set
    if [ -z "$parent_task" ] && [ "$agent_type" != "unknown" ] && [ -f "$COMM_DIR/queue.yaml" ]; then
        parent_task=$(grep -B10 "claimed_by:.*$agent_type" "$COMM_DIR/queue.yaml" 2>/dev/null | grep "task_id:" | tail -1 | cut -d':' -f2 | tr -d ' "' || echo "")
    fi

    echo "$agent_type|$agent_id|$parent_task|$run_id"
}

# =============================================================================
# LOG TO EVENTS.YAML
# =============================================================================

log_event() {
    local agent_type="$1"
    local agent_id="$2"
    local parent_task="$3"
    local event="$4"

    local events_file="$COMM_DIR/events.yaml"
    local timestamp=$(date -Iseconds)

    # Ensure directory exists
    mkdir -p "$COMM_DIR"

    # Create events.yaml if doesn't exist
    if [ ! -f "$events_file" ]; then
        echo "events:" > "$events_file"
    fi

    # Append event with file locking
    (
        flock -x 200 || exit 1
        cat >> "$events_file" << EOF

- timestamp: "$timestamp"
  type: agent_$event
  agent_type: "$agent_type"
  agent_id: "$agent_id"
  parent_task: "$parent_task"
  source: "hook"
EOF
    ) 200>"$COMM_DIR/.events.lock"

    echo "✓ Event logged: $event $agent_type"
}

# =============================================================================
# UPDATE AGENT STATE
# =============================================================================

update_agent_state() {
    local agent_type="$1"
    local event="$2"

    local state_file="$COMM_DIR/agent-state.yaml"
    local timestamp=$(date -Iseconds)

    mkdir -p "$COMM_DIR"

    # Read current state or create new with file locking
    (
        flock -x 200 || exit 1
        if [ -f "$state_file" ]; then
            # Update existing state
            if [ "$event" = "start" ]; then
                sed -i.bak "s/${agent_type}_status:.*/${agent_type}_status: active/" "$state_file" 2>/dev/null || true
                sed -i.bak "s/${agent_type}_last_start:.*/${agent_type}_last_start: $timestamp/" "$state_file" 2>/dev/null || true
                rm -f "$state_file.bak"
            else
                sed -i.bak "s/${agent_type}_status:.*/${agent_type}_status: idle/" "$state_file" 2>/dev/null || true
                sed -i.bak "s/${agent_type}_last_stop:.*/${agent_type}_last_stop: $timestamp/" "$state_file" 2>/dev/null || true
                rm -f "$state_file.bak"
            fi
        else
            # Create new state file
            cat > "$state_file" << EOF
# Agent State Tracking
# Auto-generated by subagent-tracking hook

planner_status: $([ "$agent_type" = "planner" ] && [ "$event" = "start" ] && echo "active" || echo "idle")
planner_last_start: $([ "$agent_type" = "planner" ] && [ "$event" = "start" ] && echo "$timestamp" || echo "null")
planner_last_stop: $([ "$agent_type" = "planner" ] && [ "$event" = "stop" ] && echo "$timestamp" || echo "null")

executor_status: $([ "$agent_type" = "executor" ] && [ "$event" = "start" ] && echo "active" || echo "idle")
executor_last_start: $([ "$agent_type" = "executor" ] && [ "$event" = "start" ] && echo "$timestamp" || echo "null")
executor_last_stop: $([ "$agent_type" = "executor" ] && [ "$event" = "stop" ] && echo "$timestamp" || echo "null")

architect_status: $([ "$agent_type" = "architect" ] && [ "$event" = "start" ] && echo "active" || echo "idle")
architect_last_start: $([ "$agent_type" = "architect" ] && [ "$event" = "start" ] && echo "$timestamp" || echo "null")
architect_last_stop: $([ "$agent_type" = "architect" ] && [ "$event" = "stop" ] && echo "$timestamp" || echo "null")
EOF
        fi
    ) 200>"$COMM_DIR/.agent-state.lock"
}

# =============================================================================
# MAIN
# =============================================================================

# Detect agent info
AGENT_INFO=$(detect_agent_info)
AGENT_TYPE=$(echo "$AGENT_INFO" | cut -d'|' -f1)
AGENT_ID=$(echo "$AGENT_INFO" | cut -d'|' -f2)
PARENT_TASK=$(echo "$AGENT_INFO" | cut -d'|' -f3)
RUN_ID=$(echo "$AGENT_INFO" | cut -d'|' -f4)

# Save context at session start
if [ "$EVENT_TYPE" = "start" ]; then
    save_context "$AGENT_TYPE" "$AGENT_ID" "$PARENT_TASK" "$RUN_ID"
fi

# Log event
log_event "$AGENT_TYPE" "$AGENT_ID" "$PARENT_TASK" "$EVENT_TYPE"

# Update agent state
update_agent_state "$AGENT_TYPE" "$EVENT_TYPE"

# Output for Claude
OUTPUT=$(cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "Subagent$(echo "$EVENT_TYPE" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')",
    "additionalContext": "Agent $AGENT_ID ($AGENT_TYPE) has $EVENT_TYPE. Check $COMM_DIR/agent-state.yaml for current system state.",
    "agentType": "$AGENT_TYPE",
    "agentId": "$AGENT_ID",
    "parentTask": "$PARENT_TASK"
  }
}
EOF
)

echo "$OUTPUT"
