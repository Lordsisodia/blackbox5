#!/bin/bash
# session-start-navigation.sh - Enhanced SessionStart hook
# Purpose: Discover context and inject navigation guidance
#
# Triggered by: SessionStart event
# Creates: CURRENT_CONTEXT.md in run directory

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
PARENT_PLAN=$(echo "$CONTEXT_JSON" | grep '"parent_plan"' | sed 's/.*: "\([^"]*\)".*/\1/' || echo "")
PARENT_GOAL=$(echo "$CONTEXT_JSON" | grep '"parent_goal"' | sed 's/.*: "\([^"]*\)".*/\1/' || echo "")
BLACKBOX5_DIR=$(echo "$CONTEXT_JSON" | grep '"blackbox5_dir"' | sed 's/.*: "\([^"]*\)".*/\1/' || echo "")

# Determine run directory
RUN_DIR="${RALF_RUN_DIR:-${CLAUDE_CODE_ROOT:-$(pwd)}}"

# =============================================================================
# CREATE CONTEXT FILE
# =============================================================================

if [ -n "$CURRENT_TYPE" ] && [ "$CURRENT_TYPE" != "null" ] && [ -d "$RUN_DIR" ]; then
    CONTEXT_FILE="$RUN_DIR/CURRENT_CONTEXT.md"

    cat > "$CONTEXT_FILE" << EOF
# Current Context (Auto-Generated)

## You Are Here
- **Type:** $CURRENT_TYPE
- **ID:** $CURRENT_ID

## Hierarchy
EOF

    if [ -n "$PARENT_GOAL" ] && [ "$PARENT_GOAL" != "null" ]; then
        echo "- **Goal:** $PARENT_GOAL" >> "$CONTEXT_FILE"
    fi
    if [ -n "$PARENT_PLAN" ] && [ "$PARENT_PLAN" != "null" ]; then
        echo "- **Plan:** $PARENT_PLAN" >> "$CONTEXT_FILE"
    fi
    echo "- **${CURRENT_TYPE}:** $CURRENT_ID" >> "$CONTEXT_FILE"

    cat >> "$CONTEXT_FILE" << EOF

## Quick Navigation
\`\`\`bash
bb5 whereami              # Show current location
bb5 up                    # Go up one level
bb5 root                  # Go to project root
EOF

    case "$CURRENT_TYPE" in
        goal)
            echo "bb5 plan:list             # List plans in this goal" >> "$CONTEXT_FILE"
            ;;
        plan)
            echo "bb5 task:list             # List tasks in this plan" >> "$CONTEXT_FILE"
            ;;
        task)
            echo "bb5 task:current          # Show current task details" >> "$CONTEXT_FILE"
            ;;
    esac

    echo "\`\`\`" >> "$CONTEXT_FILE"

    # Add structure validation
    cat >> "$CONTEXT_FILE" << EOF

## Structure Validation
EOF

    case "$CURRENT_TYPE" in
        goal)
            GOAL_DIR="$BLACKBOX5_DIR/goals/active/$CURRENT_ID"
            if [ ! -f "$GOAL_DIR/goal.yaml" ]; then
                echo "⚠️  Missing: goal.yaml" >> "$CONTEXT_FILE"
            else
                echo "✓ goal.yaml present" >> "$CONTEXT_FILE"
            fi
            if [ ! -f "$GOAL_DIR/timeline.yaml" ]; then
                echo "⚠️  Missing: timeline.yaml" >> "$CONTEXT_FILE"
            else
                echo "✓ timeline.yaml present" >> "$CONTEXT_FILE"
            fi
            ;;
        plan)
            PLAN_DIR="$BLACKBOX5_DIR/plans/active/$CURRENT_ID"
            if [ ! -f "$PLAN_DIR/plan.md" ] && [ ! -f "$PLAN_DIR/README.md" ]; then
                echo "⚠️  Missing: plan.md or README.md" >> "$CONTEXT_FILE"
            else
                echo "✓ Documentation present" >> "$CONTEXT_FILE"
            fi
            ;;
        task)
            TASK_DIR="$BLACKBOX5_DIR/tasks/active/$CURRENT_ID"
            if [ ! -f "$TASK_DIR/task.md" ]; then
                echo "⚠️  Missing: task.md" >> "$CONTEXT_FILE"
                echo "" >> "$CONTEXT_FILE"
                echo "Create with: bb5 task:create 'Task Name'" >> "$CONTEXT_FILE"
            else
                echo "✓ task.md present" >> "$CONTEXT_FILE"
            fi

            # Check data layers
            echo "" >> "$CONTEXT_FILE"
            echo "### Data Layers" >> "$CONTEXT_FILE"
            for file in THOUGHTS.md DECISIONS.md LEARNINGS.md; do
                if [ -f "$TASK_DIR/$file" ]; then
                    size=$(wc -l < "$TASK_DIR/$file" | tr -d ' ')
                    if [ "$size" -gt 0 ]; then
                        echo "✓ $file ($size lines)" >> "$CONTEXT_FILE"
                    else
                        echo "○ $file (empty)" >> "$CONTEXT_FILE"
                    fi
                else
                    echo "✗ $file (missing)" >> "$CONTEXT_FILE"
                fi
            done
            ;;
    esac

    echo "" >> "$CONTEXT_FILE"
    echo "---" >> "$CONTEXT_FILE"
    echo "*Context auto-generated by session-start-navigation.sh*" >> "$CONTEXT_FILE"

    echo "✓ Context discovered: $CURRENT_TYPE $CURRENT_ID"
fi

# Always succeed
echo '{"continue": true}'
