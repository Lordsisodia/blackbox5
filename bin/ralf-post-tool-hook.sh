#!/bin/bash
# ralf-post-tool-hook.sh - Post-tool hook for RALF task tracking
# Purpose: Detect file modifications during task execution and auto-update events
#
# This hook runs after each tool use in Claude Code
# It checks if files were modified and updates events.yaml accordingly

set -eo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLACKBOX5_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_DIR="${BLACKBOX5_DIR}/5-project-memory/blackbox5"
COMMS_DIR="${PROJECT_DIR}/.autonomous/agents/communications"
EVENTS_FILE="${COMMS_DIR}/events.yaml"

# Get current run info from environment (set by RALF)
RUN_ID="${RALF_RUN_ID:-unknown}"
AGENT_TYPE="${RALF_AGENT_TYPE:-unknown}"
TASK_ID="${RALF_TASK_ID:-unknown}"

# Logging function
log() {
    echo -e "${BLUE}[RALF-HOOK]${NC} $1" >&2
}

# Check if we're in a RALF context
if [[ -z "$RALF_RUN_ID" ]]; then
    # Not in RALF context, skip silently
    exit 0
fi

# Check if events.yaml exists
if [[ ! -f "$EVENTS_FILE" ]]; then
    log "Warning: events.yaml not found at $EVENTS_FILE"
    exit 0
fi

# Get git status to detect changes
# Use git diff to see what changed in the last operation
cd "$BLACKBOX5_DIR"

# Check if there are uncommitted changes
if git diff --quiet HEAD 2>/dev/null; then
    # No changes detected
    exit 0
fi

# Get list of changed files
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null | head -20)
CHANGED_COUNT=$(echo "$CHANGED_FILES" | grep -c '^' || echo "0")

if [[ "$CHANGED_COUNT" -eq 0 ]]; then
    exit 0
fi

# Determine event type based on what changed
EVENT_TYPE="file_modified"
if echo "$CHANGED_FILES" | grep -q "queue.yaml"; then
    EVENT_TYPE="queue_updated"
elif echo "$CHANGED_FILES" | grep -q "events.yaml"; then
    EVENT_TYPE="event_logged"
elif echo "$CHANGED_FILES" | grep -q "heartbeat.yaml"; then
    EVENT_TYPE="heartbeat_updated"
elif echo "$CHANGED_FILES" | grep -qE "\.(py|sh|js|ts|jsx|tsx)$"; then
    EVENT_TYPE="code_modified"
elif echo "$CHANGED_FILES" | grep -qE "\.(md|yaml|json)$"; then
    EVENT_TYPE="docs_modified"
fi

# Create event entry
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S%z")
EVENT_ENTRY=$(cat <<EOF

- timestamp: "$TIMESTAMP"
  task_id: "$TASK_ID"
  type: $EVENT_TYPE
  agent: $AGENT_TYPE
  run_id: "$RUN_ID"
  data:
    files_modified:
$(echo "$CHANGED_FILES" | sed 's/^/      - /')
    file_count: $CHANGED_COUNT
EOF
)

# Append to events.yaml
# Use a temp file to avoid race conditions
TEMP_FILE=$(mktemp)
echo "$EVENT_ENTRY" >> "$EVENTS_FILE"

log "Detected $CHANGED_COUNT file change(s) - Event logged ($EVENT_TYPE)"

# If significant changes (code or queue), also update heartbeat
if [[ "$EVENT_TYPE" == "code_modified" ]] || [[ "$EVENT_TYPE" == "queue_updated" ]]; then
    # Signal that work is happening
    touch "${COMMS_DIR}/.activity-flag"
fi

exit 0
