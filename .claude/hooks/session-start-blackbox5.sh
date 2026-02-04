#!/bin/bash
# session-start-blackbox5.sh - Smart SessionStart hook for BB5
# Purpose: Auto-detect agent type and load appropriate context
# No environment variables needed - self-discovering

set -e

# =============================================================================
# SELF-DISCOVERY: Detect agent type from context
# =============================================================================

detect_agent_type() {
    local cwd="$(pwd)"
    local run_dir="${RALF_RUN_DIR:-$cwd}"

    # Method 1: Check run directory path
    if [[ "$run_dir" == *"/planner/"* ]] || [[ "$cwd" == *"/planner/"* ]]; then
        echo "planner"
        return
    elif [[ "$run_dir" == *"/executor/"* ]] || [[ "$cwd" == *"/executor/"* ]]; then
        echo "executor"
        return
    elif [[ "$run_dir" == *"/architect/"* ]] || [[ "$cwd" == *"/architect/"* ]]; then
        echo "architect"
        return
    fi

    # Method 2: Check for agent-specific files in current directory
    if [ -f "queue.yaml" ] || [ -f "loop-metadata-template.yaml" ]; then
        echo "planner"
        return
    elif [ -f ".task-claimed" ] || ls task-*-spec.md 1>/dev/null 2>&1; then
        echo "executor"
        return
    elif [ -f "architecture-review.md" ] || [ -d "system-designs" ]; then
        echo "architect"
        return
    fi

    # Method 3: Check parent directories for agent folders
    if [[ "$cwd" == *".autonomous/agents/planner"* ]]; then
        echo "planner"
        return
    elif [[ "$cwd" == *".autonomous/agents/executor"* ]]; then
        echo "executor"
        return
    elif [[ "$cwd" == *".autonomous/agents/architect"* ]]; then
        echo "architect"
        return
    fi

    # Method 4: Check git branch name for agent hints
    local git_branch="$(git branch --show-current 2>/dev/null || echo "")"
    if [[ "$git_branch" == *"planner"* ]]; then
        echo "planner"
        return
    elif [[ "$git_branch" == *"executor"* ]]; then
        echo "executor"
        return
    elif [[ "$git_branch" == *"architect"* ]]; then
        echo "architect"
        return
    fi

    # Default: unknown
    echo "unknown"
}

# =============================================================================
# CONTEXT LOADING: Agent-specific context
# =============================================================================

load_planner_context() {
    local bb5_dir="$1"
    local context_file="$2"

    echo "## Planner Context" >> "$context_file"
    echo "" >> "$context_file"

    # Load queue status
    local queue_file="$bb5_dir/.autonomous/agents/communications/queue.yaml"
    if [ -f "$queue_file" ]; then
        local active_tasks=$(grep -c "status: pending" "$queue_file" 2>/dev/null || echo "0")
        local completed_tasks=$(grep -c "status: completed" "$queue_file" 2>/dev/null || echo "0")
        echo "**Queue Status:**" >> "$context_file"
        echo "- Active Tasks: $active_tasks" >> "$context_file"
        echo "- Completed Tasks: $completed_tasks" >> "$context_file"
        echo "" >> "$context_file"
    fi

    # Load recent loop summary
    local planner_dir="$bb5_dir/.autonomous/agents/planner"
    if [ -d "$planner_dir/runs" ]; then
        local latest_run=$(ls -1t "$planner_dir/runs" 2>/dev/null | head -1)
        if [ -n "$latest_run" ] && [ -f "$planner_dir/runs/$latest_run/THOUGHTS.md" ]; then
            echo "**Latest Loop:** $latest_run" >> "$context_file"
            echo "" >> "$context_file"
        fi
    fi

    # Load executor health
    local heartbeat_file="$bb5_dir/.autonomous/agents/communications/heartbeat.yaml"
    if [ -f "$heartbeat_file" ]; then
        local executor_status=$(grep "executor:" "$heartbeat_file" | head -1 | cut -d':' -f2 | tr -d ' ' || echo "unknown")
        echo "**Executor Status:** $executor_status" >> "$context_file"
        echo "" >> "$context_file"
    fi

    # Planner-specific commands
    echo "### Planner Commands" >> "$context_file"
    echo '```bash' >> "$context_file"
    echo "cat .autonomous/agents/communications/queue.yaml | grep -A 5 'status: pending'  # View pending tasks" >> "$context_file"
    echo "ls -lt .autonomous/agents/planner/runs/ | head -5  # Recent planner runs" >> "$context_file"
    echo "cat .autonomous/agents/communications/events.yaml | tail -20  # Recent events" >> "$context_file"
    echo '```' >> "$context_file"
}

load_executor_context() {
    local bb5_dir="$1"
    local context_file="$2"

    echo "## Executor Context" >> "$context_file"
    echo "" >> "$context_file"

    # Find claimed task
    local queue_file="$bb5_dir/.autonomous/agents/communications/queue.yaml"
    if [ -f "$queue_file" ]; then
        # Extract task claimed by this run
        local run_id="$(basename "${RALF_RUN_DIR:-$(pwd)}")"
        local claimed_task=$(awk -v run_id="$run_id" '
            /task_id:/ { task_id = $2 }
            /claimed_by:/ {
                gsub(/"/, "", $2)
                if ($2 == run_id) print task_id
            }
        ' "$queue_file" | head -1)

        if [ -n "$claimed_task" ]; then
            echo "**Claimed Task:** $claimed_task" >> "$context_file"
            echo "" >> "$context_file"

            # Load task details
            local task_file="$bb5_dir/tasks/active/$claimed_task/task.md"
            if [ -f "$task_file" ]; then
                local task_title=$(grep "^# " "$task_file" | head -1 | sed 's/^# //')
                echo "**Task Title:** $task_title" >> "$context_file"
                echo "" >> "$context_file"

                # Extract acceptance criteria
                if grep -q "Acceptance Criteria" "$task_file"; then
                    echo "**Acceptance Criteria:**" >> "$context_file"
                    sed -n '/Acceptance Criteria/,/^## /p' "$task_file" | grep "^- \[ \]" | head -5 >> "$context_file"
                    echo "" >> "$context_file"
                fi
            fi
        else
            echo "**Status:** No task claimed yet" >> "$context_file"
            echo "" >> "$context_file"
            echo "Run: bb5 task:claim  # To claim next available task" >> "$context_file"
            echo "" >> "$context_file"
        fi
    fi

    # Executor-specific commands
    echo "### Executor Commands" >> "$context_file"
    echo '```bash' >> "$context_file"
    echo "bb5 task:status        # Check claimed task status" >> "$context_file"
    echo "bb5 task:complete      # Mark task as completed" >> "$context_file"
    echo "cat .autonomous/agents/communications/queue.yaml | grep -B2 -A5 'status: pending'  # View queue" >> "$context_file"
    echo '```' >> "$context_file"
}

load_architect_context() {
    local bb5_dir="$1"
    local context_file="$2"

    echo "## Architect Context" >> "$context_file"
    echo "" >> "$context_file"

    # Load system state
    local goals_index="$bb5_dir/goals/INDEX.yaml"
    if [ -f "$goals_index" ]; then
        local active_goals=$(grep -c "status: in_progress" "$goals_index" 2>/dev/null || echo "0")
        echo "**Active Goals:** $active_goals" >> "$context_file"
        echo "" >> "$context_file"
    fi

    # Load recent decisions
    local decisions_dir="$bb5_dir/decisions"
    if [ -d "$decisions_dir" ]; then
        local recent_decision=$(ls -1t "$decisions_dir" 2>/dev/null | head -1)
        if [ -n "$recent_decision" ]; then
            echo "**Recent Decision:** $recent_decision" >> "$context_file"
            echo "" >> "$context_file"
        fi
    fi

    # Architect-specific commands
    echo "### Architect Commands" >> "$context_file"
    echo '```bash' >> "$context_file"
    echo "bb5 goal:list          # List active goals" >> "$context_file"
    echo "bb5 goal:show IG-XXX   # Show goal details" >> "$context_file"
    echo "cat goals/INDEX.yaml   # View all goals status" >> "$context_file"
    echo '```' >> "$context_file"
}

# =============================================================================
# MAIN
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BB5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"
RUN_DIR="${RALF_RUN_DIR:-$(pwd)}"

# Detect agent type
AGENT_TYPE=$(detect_agent_type)

# Create context file
CONTEXT_FILE="$RUN_DIR/AGENT_CONTEXT.md"

cat > "$CONTEXT_FILE" << EOF
# Agent Context (Auto-Generated)

**Detected Agent Type:** $AGENT_TYPE
**Run Directory:** $RUN_DIR
**Timestamp:** $(date -Iseconds)

---

EOF

# Load agent-specific context
case "$AGENT_TYPE" in
    planner)
        load_planner_context "$BB5_DIR" "$CONTEXT_FILE"
        ;;
    executor)
        load_executor_context "$BB5_DIR" "$CONTEXT_FILE"
        ;;
    architect)
        load_architect_context "$BB5_DIR" "$CONTEXT_FILE"
        ;;
    *)
        echo "**Agent Type:** Unknown - no specific context loaded" >> "$CONTEXT_FILE"
        echo "" >> "$CONTEXT_FILE"
        echo "Run 'bb5 whereami' to discover your location" >> "$CONTEXT_FILE"
        ;;
esac

# Add universal section
cat >> "$CONTEXT_FILE" << EOF

---

## Universal Commands

\`\`\`bash
bb5 whereami              # Show current location
bb5 goal:list             # List all goals
bb5 timeline recent 5     # Show recent timeline events
\`\`\`

---

*Context auto-generated by session-start-blackbox5.sh*
EOF

echo "✓ Agent context loaded: $AGENT_TYPE"
echo "  Context file: $CONTEXT_FILE"

# Return additionalContext for Claude (JSON format)
OUTPUT=$(cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "You are running as a $AGENT_TYPE agent in the BlackBox5 system. Context has been loaded from $CONTEXT_FILE. Review this file for your current tasks, queue status, and available commands.",
    "agentType": "$AGENT_TYPE",
    "contextFile": "$CONTEXT_FILE"
  }
}
EOF
)

echo "$OUTPUT"
