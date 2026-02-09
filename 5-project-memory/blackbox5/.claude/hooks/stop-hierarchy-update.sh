#!/bin/bash
# stop-hierarchy-update.sh - Enhanced Stop hook
# Purpose: Update hierarchy on session completion
#
# Triggered by: Stop event
# Updates: Parent timelines, task status

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BB5_BIN="$PROJECT_ROOT/bin"

# =============================================================================
# DISCOVER CONTEXT
# =============================================================================

# Get context from bb5-discover-context
CONTEXT_JSON=$("$BB5_BIN/bb5-discover-context" json 2>/dev/null || echo '{}')

CURRENT_TYPE=$(echo "$CONTEXT_JSON" | grep '"current_type"' | sed 's/.*: "\([^"]*\)".*/\1/' || echo "")
CURRENT_ID=$(echo "$CONTEXT_JSON" | grep '"current_id"' | sed 's/.*: "\([^"]*\)".*/\1/' || echo "")
BLACKBOX5_DIR=$(echo "$CONTEXT_JSON" | grep '"blackbox5_dir"' | sed 's/.*: "\([^"]*\)".*/\1/' || echo "")

# Find run directory
RUN_DIR="${RALF_RUN_DIR:-$(find . -maxdepth 2 -name 'run-*' -type d 2>/dev/null | head -1)}"

# =============================================================================
# UPDATE PARENT TIMELINE
# =============================================================================

if [ -n "$CURRENT_ID" ] && [ "$CURRENT_ID" != "null" ]; then
    case "$CURRENT_TYPE" in
        task)
            TASK_DIR="$BLACKBOX5_DIR/tasks/active/$CURRENT_ID"

            if [ -d "$TASK_DIR/timeline" ]; then
                # Add session completion entry
                TIMELINE_FILE="$TASK_DIR/timeline/$(date +%Y-%m-%d).md"

                # Create file if doesn't exist
                if [ ! -f "$TIMELINE_FILE" ]; then
                    echo "# Timeline: $(date +%Y-%m-%d)" > "$TIMELINE_FILE"
                    echo "" >> "$TIMELINE_FILE"
                fi

                # Add entry
                echo "" >> "$TIMELINE_FILE"
                echo "## $(date +%H:%M) - Session Completed" >> "$TIMELINE_FILE"
                echo "" >> "$TIMELINE_FILE"

                # Add summary if RESULTS.md exists
                if [ -f "$RUN_DIR/RESULTS.md" ]; then
                    echo "**Results:**" >> "$TIMELINE_FILE"
                    head -5 "$RUN_DIR/RESULTS.md" | sed 's/^/  /' >> "$TIMELINE_FILE"
                    echo "" >> "$TIMELINE_FILE"
                fi

                # Add decisions if DECISIONS.md exists
                if [ -f "$RUN_DIR/DECISIONS.md" ]; then
                    DECISION_COUNT=$(grep -c "^##" "$RUN_DIR/DECISIONS.md" 2>/dev/null || echo "0")
                    if [ "$DECISION_COUNT" -gt 0 ]; then
                        echo "**Decisions:** $DECISION_COUNT made" >> "$TIMELINE_FILE"
                    fi
                fi

                # Add link to run
                if [ -n "$RUN_DIR" ] && [ "$RUN_DIR" != "." ]; then
                    echo "" >> "$TIMELINE_FILE"
                    echo "[View Run]($RUN_DIR)" >> "$TIMELINE_FILE"
                fi

                echo "✓ Updated task timeline: $CURRENT_ID"
            fi

            # Check if task is complete (has RESULTS.md with completion)
            if [ -f "$RUN_DIR/RESULTS.md" ]; then
                if grep -qi "complete\|done\|finished" "$RUN_DIR/RESULTS.md"; then
                    # Update task.md status
                    TASK_FILE="$TASK_DIR/task.md"
                    if [ -f "$TASK_FILE" ]; then
                        # Update status to completed
                        sed -i '' 's/Status: in_progress/Status: completed/g' "$TASK_FILE" 2>/dev/null || true
                        sed -i '' 's/Status: pending/Status: completed/g' "$TASK_FILE" 2>/dev/null || true
                        echo "✓ Marked task as completed: $CURRENT_ID"
                    fi
                fi
            fi
            ;;

        plan)
            PLAN_DIR="$BLACKBOX5_DIR/plans/active/$CURRENT_ID"

            # Update plan metadata if results exist
            if [ -f "$RUN_DIR/RESULTS.md" ] && [ -f "$PLAN_DIR/metadata.yaml" ]; then
                # Add last_updated timestamp
                sed -i '' "s/last_updated:.*/last_updated: $(date +%Y-%m-%d)/g" "$PLAN_DIR/metadata.yaml" 2>/dev/null || true
                echo "✓ Updated plan metadata: $CURRENT_ID"
            fi
            ;;

        goal)
            GOAL_DIR="$BLACKBOX5_DIR/goals/active/$CURRENT_ID"

            # Update goal timeline
            if [ -f "$GOAL_DIR/timeline.yaml" ]; then
                # Add entry using Python for YAML manipulation
                python3 << PYEOF 2>/dev/null || true
import yaml
from datetime import datetime

timeline_file = "$GOAL_DIR/timeline.yaml"
try:
    with open(timeline_file, 'r') as f:
        data = yaml.safe_load(f) or {"timeline": []}

    data["timeline"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "event": "Session completed",
        "time": datetime.now().strftime("%H:%M")
    })

    with open(timeline_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
except Exception as e:
    pass
PYEOF
                echo "✓ Updated goal timeline: $CURRENT_ID"
            fi
            ;;
    esac
fi

# Always succeed
echo "✓ Hierarchy update complete"
