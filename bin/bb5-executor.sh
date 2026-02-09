#!/bin/bash
# BB5 Executor - Executes improvement tasks using Claude/GLM
# This script processes improvement tasks and executes them

set -e

# Source common library for shared functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/bb5-common.sh"

# Initialize
BB5_SCRIPT_NAME="BB5-EXECUTOR"
bb5_init_logging "bb5-executor"
bb5_ensure_directories

# Alias bb5_log for backward compatibility
log() {
    bb5_log "$1"
}

log "═══════════════════════════════════════════════════"
log "BB5 Executor Starting"
log "═══════════════════════════════════════════════════"

# Detect AI provider
if command -v claude &> /dev/null; then
    AI_PROVIDER="claude"
    log "✓ Using Claude Code"
elif command -v glm &> /dev/null; then
    AI_PROVIDER="glm"
    log "✓ Using GLM-4.7"
else
    log "❌ No AI provider found"
    exit 1
fi

LOOP_COUNT=0
while true; do
    LOOP_COUNT=$((LOOP_COUNT + 1))
    RUN_FOLDER=$(bb5_create_run_folder)
    RUN_ID=$(basename "$RUN_FOLDER" | sed 's/run-//')

    log ""
    log "═══════════════════════════════════════════════════"
    log "Execution Cycle $LOOP_COUNT - Run $RUN_ID"
    log "═══════════════════════════════════════════════════"

    # Pull latest
    bb5_git_pull "$RUN_FOLDER/git.log" || log "Pull failed"

    # Find pending improvement tasks
    PENDING_TASK=$(bb5_get_pending_task)

    if [ -z "$PENDING_TASK" ]; then
        log "No pending improvement tasks found"
        log "Waiting for bb5-simple-improver to create tasks..."
        sleep 60
        continue
    fi

    TASK_NAME=$(basename "$PENDING_TASK" .md)
    log "Found pending task: $TASK_NAME"

    # Read task content
    TASK_CONTENT=$(cat "$PENDING_TASK")

    # Create execution prompt
    cat > "$RUN_FOLDER/execution-prompt.md" << EOF
You are the BB5 Executor Agent. Your job is to implement improvements to BlackBox5.

## Task to Execute

$TASK_CONTENT

## Instructions

1. Read the task description carefully
2. Analyze the current state of BB5 related to this task
3. Implement the improvements described
4. Make SMALL, focused changes (30 minutes max)
5. Test your changes if applicable
6. Update documentation
7. Commit changes with descriptive message

## Guidelines

- Focus on ONE specific improvement
- Don't break existing functionality
- Document what you do
- Commit frequently
- Push to the vps branch

## Output

Create the following in $RUN_FOLDER:
- THOUGHTS.md - Your reasoning
- DECISIONS.md - What you decided
- LEARNINGS.md - What you learned
- RESULTS.md - What was accomplished
- status.txt - COMPLETED, PARTIAL, or FAILED

When done, move $PENDING_TASK to $ACTIVE_DIR/completed/

Start executing now.
EOF

    log "Executing task with $AI_PROVIDER..."

    export BB5_RUN_FOLDER="$RUN_FOLDER"
    export BB5_TASK="$TASK_NAME"

    if [ "$AI_PROVIDER" = "claude" ]; then
        # Run Claude as bb5-runner with bypass permissions for full autonomy
        log "Running Claude as bb5-runner with bypass permissions..."
        chown -R bb5-runner:bb5-runner "$RUN_FOLDER"
        if sudo -u bb5-runner -H /usr/local/bin/claude -p --dangerously-skip-permissions < "$RUN_FOLDER/execution-prompt.md" 2>&1 | tee "$RUN_FOLDER/execution.log"; then
            log "✓ Claude execution completed"
        else
            log "❌ Claude execution failed"
            echo "FAILED" > "$RUN_FOLDER/status.txt"
        fi
    elif [ "$AI_PROVIDER" = "glm" ]; then
        if glm chat --model 4.7 < "$RUN_FOLDER/execution-prompt.md" 2>&1 | tee "$RUN_FOLDER/execution.log"; then
            log "✓ GLM execution completed"
        else
            log "❌ GLM execution failed"
            echo "FAILED" > "$RUN_FOLDER/status.txt"
        fi
    fi

    # Check status
    if [ -f "$RUN_FOLDER/status.txt" ]; then
        FINAL_STATUS=$(cat "$RUN_FOLDER/status.txt")
    else
        FINAL_STATUS="PARTIAL"
        echo "$FINAL_STATUS" > "$RUN_FOLDER/status.txt"
    fi

    log "Execution status: $FINAL_STATUS"

    # Move task to completed if successful
    if [ "$FINAL_STATUS" = "COMPLETED" ]; then
        bb5_complete_task "$PENDING_TASK"
        log "✓ Task moved to completed"
    fi

    # Commit and push using common library
    bb5_git_commit "bb5-executor: [$RUN_ID] $TASK_NAME - $FINAL_STATUS" || true
    bb5_git_push "$RUN_FOLDER/git.log" || log "Push failed"

    log ""
    log "═══════════════════════════════════════════════════"
    log "Cycle $LOOP_COUNT Complete - Status: $FINAL_STATUS"
    log "═══════════════════════════════════════════════════"

    # Sleep before next cycle
    sleep 300  # 5 minutes
done
