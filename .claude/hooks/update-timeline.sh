#!/bin/bash
#
# Blackbox5 Hook: Update Timeline with Session Event
# Event: SessionEnd
# Purpose: Add session event to project timeline
#

set -euo pipefail

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')

MEMORY_BASE="${BLACKBOX5_MEMORY_PATH:-./blackbox5/5-project-memory/siso-internal}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

TIMELINE_FILE="$MEMORY_BASE/project/timeline.yaml"

if [[ ! -f "$TIMELINE_FILE" ]]; then
    exit 0
fi

if command -v yq >/dev/null 2>&1; then
    yq eval ".events += [{\"date\": \"$TIMESTAMP\", \"type\": \"session\", \"title\": \"Session completed: $SESSION_ID\", \"description\": \"Claude Code session ended\", \"impact\": \"low\"}]" -i "$TIMELINE_FILE"
else
    echo "" >> "$TIMELINE_FILE"
    echo "events:" >> "$TIMELINE_FILE"
    echo "  - date: \"$TIMESTAMP\"" >> "$TIMELINE_FILE"
    echo "    type: \"session\"" >> "$TIMELINE_FILE"
    echo "    title: \"Session completed: $SESSION_ID\"" >> "$TIMELINE_FILE"
    echo "    description: \"Claude Code session ended\"" >> "$TIMELINE_FILE"
    echo "    impact: \"low\"" >> "$TIMELINE_FILE"
fi

exit 0
