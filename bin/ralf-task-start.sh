#!/bin/bash
# RALF Task Start Script
# Marks a task as in_progress when executor begins work
# Usage: ralf-task-start.sh --task-id TASK-XXX

set -e

# Configuration
PROJECT_NAME="${RALF_PROJECT_NAME:-blackbox5}"
AGENT_TYPE="${RALF_AGENT_TYPE:-executor}"
RUN_ID="${RALF_RUN_ID:-unknown}"

# Project root detection
if [ -n "$RALF_PROJECT_ROOT" ]; then
    PROJECT_ROOT="$RALF_PROJECT_ROOT"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

# Paths
COMMUNICATIONS_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/communications"
QUEUE_FILE="$COMMUNICATIONS_DIR/queue.yaml"
EVENTS_FILE="$COMMUNICATIONS_DIR/events.yaml"
HEARTBEAT_FILE="$COMMUNICATIONS_DIR/heartbeat.yaml"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[TASK-START]${NC} $1"; }
success() { echo -e "${GREEN}[TASK-START]${NC} $1"; }
warning() { echo -e "${YELLOW}[TASK-START]${NC} $1"; }

# Parse arguments
TASK_ID=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --task-id)
            TASK_ID="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 --task-id TASK-XXX"
            exit 1
            ;;
    esac
done

if [ -z "$TASK_ID" ]; then
    # Try to get from environment
    if [ -n "$RALF_TASK_ID" ]; then
        TASK_ID="$RALF_TASK_ID"
    else
        echo "Error: No task ID provided"
        echo "Usage: $0 --task-id TASK-XXX"
        exit 1
    fi
fi

log "Starting work on task: $TASK_ID"

TIMESTAMP=$(date -Iseconds)

# Update queue.yaml - set task status to in_progress
if [ -f "$QUEUE_FILE" ]; then
    awk -F': ' -v task_id="$TASK_ID" -v timestamp="$TIMESTAMP" '
        /^  - task_id: / {
            in_target_task = ($2 == task_id)
        }
        in_target_task && /^    status: / {
            print "    status: in_progress"
            print "    started_at: \"" timestamp "\""
            next
        }
        { print }
    ' "$QUEUE_FILE" > "$QUEUE_FILE.tmp" && mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"

    success "Task status updated to 'in_progress' in queue.yaml"
fi

# Log event
if [ -f "$EVENTS_FILE" ]; then
    cat >> "$EVENTS_FILE" << EOF

- timestamp: "$TIMESTAMP"
  task_id: "$TASK_ID"
  type: in_progress
  agent: executor
  run_id: "$RUN_ID"
EOF
    success "Event logged to events.yaml"
fi

# Update heartbeat
if [ -f "$HEARTBEAT_FILE" ]; then
    sed -i.bak "s/status: .*/status: in_progress_$TASK_ID/" "$HEARTBEAT_FILE" 2>/dev/null || true
    rm -f "$HEARTBEAT_FILE.bak"
    success "Heartbeat updated"
fi

echo ""
success "Task $TASK_ID is now in progress"
