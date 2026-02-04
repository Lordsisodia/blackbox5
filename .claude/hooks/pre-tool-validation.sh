#!/bin/bash
# pre-tool-validation.sh - PreToolUse hook for structure validation
# Purpose: Validate tool use against hierarchy structure
#
# Triggered by: PreToolUse event
# Validates: Write operations, Task creation, Bash commands

set -e

# =============================================================================
# READ INPUT
# =============================================================================

INPUT=$(head -c 100000)  # Security: limit input size
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || echo "")

# =============================================================================
# VALIDATIONS
# =============================================================================

WARNINGS=""

# Validate Write operations
if [ "$TOOL_NAME" = "Write" ]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

    # Check if writing to tasks/ without task.md
    if echo "$FILE_PATH" | grep -q "/tasks/active/" && ! echo "$FILE_PATH" | grep -q "task.md"; then
        # Extract task directory
        TASK_PATH=$(echo "$FILE_PATH" | grep -oE '/tasks/active/[^/]+' | head -1)
        if [ -n "$TASK_PATH" ]; then
            TASK_DIR="${PROJECT_ROOT:-$HOME/.blackbox5/5-project-memory/blackbox5}$TASK_PATH"
            if [ ! -f "$TASK_DIR/task.md" ]; then
                WARNINGS="${WARNINGS}⚠️  Writing to task directory without task.md: $(basename "$TASK_DIR")\n"
                WARNINGS="${WARNINGS}   Run: bb5 task:create 'Task Name' first\n"
            fi
        fi
    fi

    # Check if writing to goals/ without goal.yaml
    if echo "$FILE_PATH" | grep -q "/goals/active/" && ! echo "$FILE_PATH" | grep -q "goal.yaml"; then
        GOAL_PATH=$(echo "$FILE_PATH" | grep -oE '/goals/active/[^/]+' | head -1)
        if [ -n "$GOAL_PATH" ]; then
            GOAL_DIR="${PROJECT_ROOT:-$HOME/.blackbox5/5-project-memory/blackbox5}$GOAL_PATH"
            if [ ! -f "$GOAL_DIR/goal.yaml" ]; then
                WARNINGS="${WARNINGS}⚠️  Writing to goal directory without goal.yaml: $(basename "$GOAL_DIR")\n"
                WARNINGS="${WARNINGS}   Run: bb5 goal:create 'Goal Name' first\n"
            fi
        fi
    fi
fi

# Validate Task creation
if [ "$TOOL_NAME" = "Task" ]; then
    TASK_PROMPT=$(echo "$INPUT" | jq -r '.tool_input.prompt // ""' 2>/dev/null || echo "")

    # Check if creating a task without proper context
    if echo "$TASK_PROMPT" | grep -qi "implement\|fix\|refactor"; then
        # Check if we're in a task directory
        CWD=$(pwd)
        if ! echo "$CWD" | grep -q "/tasks/active/"; then
            WARNINGS="${WARNINGS}💡 Creating a task implementation outside of task directory\n"
            WARNINGS="${WARNINGS}   Consider: cd tasks/active/TASK-XXX first\n"
        fi
    fi
fi

# =============================================================================
# OUTPUT
# =============================================================================

if [ -n "$WARNINGS" ]; then
    echo "$WARNINGS" >&2
fi

# Always allow (just warn)
echo '{"continue": true}'
