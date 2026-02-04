#!/bin/bash
# context-synchronization.sh - PostToolUse hook for context sync
# Purpose: Synchronize context across files when changes occur
#
# Triggered by: PostToolUse event (after Write, Edit, TaskUpdate)
# Syncs: Goal progress, task status, timeline entries, index updates

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

# =============================================================================
# SYNCHRONIZATION FUNCTIONS
# =============================================================================

sync_goal_progress() {
    local file_path="$1"

    # If task completed, update parent goal progress
    if echo "$file_path" | grep -qE "/tasks/active/[^/]+/task\.md$"; then
        local task_dir=$(dirname "$file_path")
        local task_id=$(basename "$task_dir")

        # Find parent goal via symlinks
        for goal_dir in "$BB5_DIR"/goals/active/*; do
            if [ -d "$goal_dir/plans" ]; then
                for plan_link in "$goal_dir/plans"/*; do
                    if [ -L "$plan_link" ]; then
                        local plan_tasks_dir=$(readlink "$plan_link")/tasks
                        if [ -d "$plan_tasks_dir/$task_id" ]; then
                            local goal_id=$(basename "$goal_dir")
                            echo "✓ Task $task_id linked to goal $goal_id - consider updating goal progress"
                        fi
                    fi
                done
            fi
        done
    fi
}

sync_index_updates() {
    local file_path="$1"

    # Check if goal/plan/task modified that should trigger INDEX.yaml update
    if echo "$file_path" | grep -qE "/(goals|plans|tasks)/active/"; then
        echo "💡 INDEX.yaml may need regeneration (goal/plan/task modified)"
        echo "   Run: bb5 index:regenerate"
    fi
}

sync_timeline_context() {
    local file_path="$1"

    # If working in a task, update its timeline
    if echo "$file_path" | grep -qE "/tasks/active/[^/]+/"; then
        local task_dir=$(echo "$file_path" | grep -oE "/tasks/active/[^/]+" | head -1)
        local full_task_dir="${BB5_DIR}${task_dir}"
        local timeline_dir="$full_task_dir/timeline"

        if [ -d "$timeline_dir" ]; then
            local today_file="$timeline_dir/$(date +%Y-%m-%d).md"

            # Create today's timeline file if it doesn't exist
            if [ ! -f "$today_file" ]; then
                echo "# Timeline: $(date +%Y-%m-%d)" > "$today_file"
                echo "" >> "$today_file"
                echo "## $(date +%H:%M) - Session Started" >> "$today_file"
                echo "" >> "$today_file"
                echo "Working on: $(basename "$file_path")" >> "$today_file"
                echo "✓ Created timeline entry: $(basename "$today_file")"
            fi
        fi
    fi
}

sync_core_goal_metrics() {
    local file_path="$1"

    # If completing a task linked to a core goal initiative, suggest metric update
    if echo "$file_path" | grep -qE "/tasks/active/[^/]+/task\.md$"; then
        if grep -q "Status.*completed" "$file_path" 2>/dev/null; then
            local task_id=$(basename "$(dirname "$file_path")")

            # Check if task is linked to core goals
            for core_goal_file in "$BB5_DIR"/goals/core/*.yaml; do
                if [ -f "$core_goal_file" ]; then
                    if grep -q "$task_id" "$core_goal_file" 2>/dev/null; then
                        local core_goal=$(grep "^  - id:" "$core_goal_file" | head -1 | sed 's/.*id: //')
                        echo "📊 Task $task_id linked to $core_goal - consider updating core goal metrics"
                    fi
                fi
            done
        fi
    fi
}

# =============================================================================
# MAIN SYNCHRONIZATION
# =============================================================================

if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

    if [ -n "$FILE_PATH" ]; then
        sync_goal_progress "$FILE_PATH"
        sync_index_updates "$FILE_PATH"
        sync_timeline_context "$FILE_PATH"
        sync_core_goal_metrics "$FILE_PATH"
    fi
fi

if [ "$TOOL_NAME" = "TaskUpdate" ]; then
    TASK_ID=$(echo "$INPUT" | jq -r '.tool_input.taskId // empty' 2>/dev/null || echo "")
    NEW_STATUS=$(echo "$INPUT" | jq -r '.tool_input.status // empty' 2>/dev/null || echo "")

    if [ "$NEW_STATUS" = "completed" ] && [ -n "$TASK_ID" ]; then
        echo "✓ Task $TASK_ID completed - check if parent goals need progress updates"
    fi
fi

# Always succeed
echo '{"continue": true}'
