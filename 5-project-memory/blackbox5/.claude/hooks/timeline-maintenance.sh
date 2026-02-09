#!/bin/bash
# timeline-maintenance.sh - PostToolUse hook for timeline updates
# Purpose: Automatically update project timeline on significant events
#
# Triggered by: PostToolUse event (after Write, Edit, TaskUpdate)
# Updates: timeline.yaml with new events

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TIMELINE_FILE="$PROJECT_ROOT/5-project-memory/blackbox5/timeline.yaml"

# =============================================================================
# READ INPUT
# =============================================================================

INPUT=$(head -c 100000)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
TOOL_OUTPUT=$(echo "$INPUT" | jq -r '.tool_output // empty' 2>/dev/null || echo "")

# =============================================================================
# DETECT SIGNIFICANT EVENTS
# =============================================================================

EVENT_TYPE=""
EVENT_TITLE=""
EVENT_DESCRIPTION=""
EVENT_IMPACT="medium"
RELATED_ITEMS=""

case "$TOOL_NAME" in
    "Write"|"Edit")
        FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

        # Detect goal creation
        if echo "$FILE_PATH" | grep -qE "/goals/active/[^/]+/goal\.yaml$"; then
            GOAL_ID=$(basename "$(dirname "$FILE_PATH")")
            EVENT_TYPE="milestone"
            EVENT_TITLE="Goal Created: $GOAL_ID"
            EVENT_DESCRIPTION="New implementation goal created and activated"
            EVENT_IMPACT="medium"
            RELATED_ITEMS="$GOAL_ID"
        fi

        # Detect task completion (status change to completed)
        if echo "$FILE_PATH" | grep -qE "/tasks/active/[^/]+/task\.md$"; then
            if echo "$TOOL_OUTPUT" | grep -q "Status.*completed"; then
                TASK_ID=$(basename "$(dirname "$FILE_PATH")")
                EVENT_TYPE="milestone"
                EVENT_TITLE="Task Completed: $TASK_ID"
                EVENT_DESCRIPTION="Task marked as completed"
                EVENT_IMPACT="low"
                RELATED_ITEMS="$TASK_ID"
            fi
        fi

        # Detect timeline.yaml updates (avoid recursive updates)
        if echo "$FILE_PATH" | grep -q "timeline.yaml$"; then
            # Don't trigger on timeline updates
            EVENT_TYPE=""
        fi

        # Detect architecture changes (DECISIONS.md, architecture docs)
        if echo "$FILE_PATH" | grep -qE "(DECISIONS|ARCHITECTURE|STRUCTURE)"; then
            EVENT_TYPE="decision"
            EVENT_TITLE="Architecture Decision Recorded"
            EVENT_DESCRIPTION="New architectural decision documented"
            EVENT_IMPACT="high"
        fi
        ;;

    "TaskUpdate")
        TASK_ID=$(echo "$INPUT" | jq -r '.tool_input.taskId // empty' 2>/dev/null || echo "")
        NEW_STATUS=$(echo "$INPUT" | jq -r '.tool_input.status // empty' 2>/dev/null || echo "")

        if [ "$NEW_STATUS" = "completed" ]; then
            EVENT_TYPE="milestone"
            EVENT_TITLE="Task Completed: $TASK_ID"
            EVENT_DESCRIPTION="Task marked as completed via TaskUpdate"
            EVENT_IMPACT="low"
            RELATED_ITEMS="$TASK_ID"
        elif [ "$NEW_STATUS" = "in_progress" ]; then
            EVENT_TYPE="process"
            EVENT_TITLE="Task Started: $TASK_ID"
            EVENT_DESCRIPTION="Task work initiated"
            EVENT_IMPACT="low"
            RELATED_ITEMS="$TASK_ID"
        fi
        ;;

    "TaskCreate")
        EVENT_TYPE="process"
        EVENT_TITLE="New Task Created"
        EVENT_DESCRIPTION="Task added to active queue"
        EVENT_IMPACT="low"
        ;;

esac

# =============================================================================
# UPDATE TIMELINE
# =============================================================================

if [ -n "$EVENT_TYPE" ] && [ -f "$TIMELINE_FILE" ]; then
    # Create temp file for new event
    TEMP_FILE=$(mktemp)

    cat >> "$TEMP_FILE" << EOF

  - date: "$(date +%Y-%m-%d)"
    type: "$EVENT_TYPE"
    title: "$EVENT_TITLE"
    description: "$EVENT_DESCRIPTION"
    impact: "$EVENT_IMPACT"
EOF

    if [ -n "$RELATED_ITEMS" ]; then
        echo "    related_items:" >> "$TEMP_FILE"
        echo "      - \"$RELATED_ITEMS\"" >> "$TEMP_FILE"
    else
        echo "    related_items: null" >> "$TEMP_FILE"
    fi

    # Insert before the progress section (find the line with "# PROGRESS METRICS")
    awk '
        /^# =+$/ { if (found_events) { print; while ((getline line < tmpfile) > 0) print line; close(tmpfile); found_events=0 } }
        /^# PROGRESS METRICS/ { found_events=1 }
        { print }
    ' tmpfile="$TEMP_FILE" "$TIMELINE_FILE" > "${TIMELINE_FILE}.tmp"

    mv "${TIMELINE_FILE}.tmp" "$TIMELINE_FILE"
    rm -f "$TEMP_FILE"

    echo "✓ Timeline updated: $EVENT_TITLE"
fi

# Always succeed
echo '{"continue": true}'
