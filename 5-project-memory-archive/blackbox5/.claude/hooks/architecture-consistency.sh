#!/bin/bash
# architecture-consistency.sh - PreToolUse hook for architecture validation
# Purpose: Validate that changes maintain system architecture consistency
#
# Triggered by: PreToolUse event (before Write, Edit, Bash)
# Validates: Directory structure, naming conventions, hierarchy integrity

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BB5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"

# =============================================================================
# READ INPUT
# =============================================================================

INPUT=$(head -c 100000)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || echo "")

WARNINGS=""
SUGGESTIONS=""

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

validate_goal_structure() {
    local file_path="$1"

    # Check if creating goal without proper structure
    if echo "$file_path" | grep -qE "/goals/active/[^/]+/"; then
        local goal_dir=$(echo "$file_path" | grep -oE "/goals/active/[^/]+" | head -1)
        local full_goal_dir="${BB5_DIR}${goal_dir}"

        # Check for required files
        if [ ! -f "$full_goal_dir/goal.yaml" ] && [ "$file_path" != "$full_goal_dir/goal.yaml" ]; then
            WARNINGS="${WARNINGS}⚠️  Creating files in goal directory without goal.yaml\n"
            SUGGESTIONS="${SUGGESTIONS}  → Run: bb5 goal:create 'Goal Name' first\n"
        fi

        # Check for required subdirectories
        if [ -d "$full_goal_dir" ]; then
            if [ ! -d "$full_goal_dir/plans" ]; then
                SUGGESTIONS="${SUGGESTIONS}  → Missing: plans/ subdirectory\n"
            fi
            if [ ! -d "$full_goal_dir/journal" ]; then
                SUGGESTIONS="${SUGGESTIONS}  → Missing: journal/ subdirectory\n"
            fi
        fi
    fi
}

validate_plan_structure() {
    local file_path="$1"

    if echo "$file_path" | grep -qE "/plans/active/[^/]+/"; then
        local plan_dir=$(echo "$file_path" | grep -oE "/plans/active/[^/]+" | head -1)
        local full_plan_dir="${BB5_DIR}${plan_dir}"

        if [ ! -f "$full_plan_dir/plan.md" ] && [ ! -f "$full_plan_dir/README.md" ] && \
           [ "$file_path" != "$full_plan_dir/plan.md" ] && [ "$file_path" != "$full_plan_dir/README.md" ]; then
            WARNINGS="${WARNINGS}⚠️  Creating files in plan directory without plan.md\n"
            SUGGESTIONS="${SUGGESTIONS}  → Run: bb5 plan:create 'Plan Name' first\n"
        fi

        if [ -d "$full_plan_dir" ]; then
            if [ ! -d "$full_plan_dir/tasks" ]; then
                SUGGESTIONS="${SUGGESTIONS}  → Missing: tasks/ subdirectory\n"
            fi
        fi
    fi
}

validate_task_structure() {
    local file_path="$1"

    if echo "$file_path" | grep -qE "/tasks/active/[^/]+/"; then
        local task_dir=$(echo "$file_path" | grep -oE "/tasks/active/[^/]+" | head -1)
        local full_task_dir="${BB5_DIR}${task_dir}"

        if [ ! -f "$full_task_dir/task.md" ] && [ "$file_path" != "$full_task_dir/task.md" ]; then
            WARNINGS="${WARNINGS}⚠️  Creating files in task directory without task.md\n"
            SUGGESTIONS="${SUGGESTIONS}  → Run: bb5 task:create 'Task Name' first\n"
        fi

        if [ -d "$full_task_dir" ]; then
            if [ ! -d "$full_task_dir/timeline" ]; then
                SUGGESTIONS="${SUGGESTIONS}  → Missing: timeline/ subdirectory\n"
            fi
            if [ ! -d "$full_task_dir/subtasks" ]; then
                SUGGESTIONS="${SUGGESTIONS}  → Missing: subtasks/ subdirectory\n"
            fi
        fi
    fi
}

validate_naming_conventions() {
    local file_path="$1"

    # Check goal naming (IG-XXX)
    if echo "$file_path" | grep -q "/goals/active/"; then
        local goal_name=$(echo "$file_path" | grep -oE "goals/active/[^/]+" | cut -d'/' -f3)
        if [ -n "$goal_name" ] && ! echo "$goal_name" | grep -qE "^(CG|IG)-[0-9]+$"; then
            WARNINGS="${WARNINGS}⚠️  Goal name '$goal_name' doesn't follow convention (CG-XXX or IG-XXX)\n"
        fi
    fi

    # Check task naming (TASK-XXX)
    if echo "$file_path" | grep -q "/tasks/active/"; then
        local task_name=$(echo "$file_path" | grep -oE "tasks/active/[^/]+" | cut -d'/' -f3)
        if [ -n "$task_name" ] && ! echo "$task_name" | grep -qE "^TASK-[0-9]+$"; then
            WARNINGS="${WARNINGS}⚠️  Task name '$task_name' doesn't follow convention (TASK-XXX)\n"
        fi
    fi
}

validate_symlink_integrity() {
    local file_path="$1"

    # Check if modifying a symlinked file
    if [ -L "$file_path" ]; then
        local target=$(readlink "$file_path")
        WARNINGS="${WARNINGS}⚠️  Modifying a symlink: $file_path → $target\n"
        SUGGESTIONS="${SUGGESTIONS}  → Consider modifying the target file instead\n"
    fi
}

# =============================================================================
# MAIN VALIDATION
# =============================================================================

if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

    if [ -n "$FILE_PATH" ]; then
        validate_goal_structure "$FILE_PATH"
        validate_plan_structure "$FILE_PATH"
        validate_task_structure "$FILE_PATH"
        validate_naming_conventions "$FILE_PATH"
        validate_symlink_integrity "$FILE_PATH"
    fi
fi

# =============================================================================
# OUTPUT
# =============================================================================

if [ -n "$WARNINGS" ]; then
    echo "Architecture Consistency Check:" >&2
    echo -e "$WARNINGS" >&2
    if [ -n "$SUGGESTIONS" ]; then
        echo "Suggestions:" >&2
        echo -e "$SUGGESTIONS" >&2
    fi
    echo "" >&2
fi

# Always allow (just warn)
echo '{"continue": true}'
