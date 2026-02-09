#!/bin/bash
# RALF-Core: BB5 Autonomous Task Execution Loop
# Inspired by ralphy - runs Claude Code in a loop until all tasks complete

set -eo pipefail

# Configuration
BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
TASKS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/tasks"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"
QUEUE_FILE="$BB5_DIR/5-project-memory/blackbox5/.autonomous/communications/queue-core.yaml"
LOG_FILE="$BB5_DIR/.autonomous/logs/ralf-core.log"
MAX_RETRIES=3
RETRY_DELAY=10

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1" | tee -a "$LOG_FILE"
}

# Ensure directories exist
mkdir -p "$TASKS_DIR/active" "$TASKS_DIR/completed" "$RUNS_DIR"
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$QUEUE_FILE")"

# Detect AI provider
detect_ai_provider() {
    if [ -n "$ANTHROPIC_API_KEY" ] && command -v claude &> /dev/null; then
        echo "claude"
    elif command -v glm &> /dev/null; then
        echo "glm"
    else
        echo "none"
    fi
}

AI_PROVIDER=$(detect_ai_provider)

# Find the highest priority pending/partial task
find_next_task() {
    local highest_priority_task=""
    local highest_priority=999
    local priority_value

    # Scan all task files recursively using a temp file approach
    local tmpfile=$(mktemp)
    find "$TASKS_DIR/active" -name "TASK-*.md" -type f > "$tmpfile" 2>/dev/null

    while IFS= read -r task_file; do
        # Skip files in runs.migrated or completed directories
        if [[ "$task_file" == *"/runs.migrated/"* ]] || [[ "$task_file" == *"/completed/"* ]]; then
            continue
        fi

        # Extract status from task file (use simple grep to avoid regex escaping issues)
        local status_line=$(grep 'Status:' "$task_file" 2>/dev/null | grep -E '(pending|partial)' | head -1 || echo "")
        local status=$(echo "$status_line" | sed 's/.*://' | tr -d '[:space:]*' || echo "")

        if [ -n "$status" ]; then
            # Extract priority
            local priority=$(grep 'Priority:' "$task_file" 2>/dev/null | head -1 | sed 's/.*://' | tr -d '[:space:]*' | tr '[:upper:]' '[:lower:]' || echo "medium")

            # Convert priority to numeric value
            case "$priority" in
                critical) priority_value=1 ;;
                high) priority_value=2 ;;
                medium) priority_value=3 ;;
                low) priority_value=4 ;;
                *) priority_value=5 ;;
            esac

            if [ "$priority_value" -lt "$highest_priority" ]; then
                highest_priority="$priority_value"
                highest_priority_task="$task_file"
            fi
        fi
    done < "$tmpfile"

    rm -f "$tmpfile"
    echo "$highest_priority_task"
}

# Count remaining tasks
count_remaining_tasks() {
    local count=0
    local tmpfile=$(mktemp)
    find "$TASKS_DIR/active" -name "TASK-*.md" -type f > "$tmpfile" 2>/dev/null

    while IFS= read -r task_file; do
        if [[ "$task_file" == *"/runs.migrated/"* ]] || [[ "$task_file" == *"/completed/"* ]]; then
            continue
        fi
        if grep 'Status:' "$task_file" 2>/dev/null | grep -qE '(pending|partial)'; then
            count=$((count + 1))
        fi
    done < "$tmpfile"

    rm -f "$tmpfile"
    echo "$count"
}

# Build the execution prompt for Claude
build_prompt() {
    local task_file="$1"
    local run_folder="$2"
    local task_id=$(basename "$task_file" .md)
    local task_content=$(cat "$task_file")

    cat << EOF
You are the BB5 Autonomous Executor. Your mission is to execute tasks and improve the BlackBox5 system.

## Current Task

Task File: $task_file
Run Folder: $run_folder

$task_content

## Instructions

1. Read the task description carefully
2. Analyze the current BB5 state related to this task
3. Implement the improvements described
4. Make SMALL, focused changes (30 minutes max)
5. Test your changes if applicable
6. Update the task file to mark it as complete:
   - Change **Status:** from pending/partial to completed
   - Add a summary of what was done
7. Document your work in the run folder:
   - $run_folder/THOUGHTS.md - Your reasoning
   - $run_folder/DECISIONS.md - What you decided
   - $run_folder/LEARNINGS.md - What you learned
   - $run_folder/RESULTS.md - What was accomplished
8. Commit changes with a descriptive message

## Critical Rules

- ONLY work on THIS specific task
- Do NOT modify other tasks
- Do NOT break existing functionality
- If you cannot complete the task, mark it as partial and explain why
- When done, output: <promise>COMPLETE</promise>
- If partially done, output: <promise>PARTIAL</promise>

## Git Commands

After making changes:
\`\`\`bash
git add -A
git commit -m "ralf: [$task_id] brief description of changes"
\`\`\`

Begin execution now.
EOF
}

# Run Claude Code with the prompt
run_claude() {
    local prompt="$1"
    local output_file="$2"

    log "Running Claude Code..."

    # Use cheaper model for most tasks, allow override for complex tasks
    local model="${CLAUDE_MODEL:-glm-4.7-flash}"

    # Run Claude with the prompt and model
    if echo "$prompt" | claude -p --dangerously-skip-permissions --model "$model" > "$output_file" 2>&1; then
        return 0
    else
        return 1
    fi
}

# Execute a single task
execute_task() {
    local task_file="$1"
    local iteration="$2"
    local task_id=$(basename "$task_file" .md)
    local run_id=$(date +"%Y%m%d_%H%M%S")
    local run_folder="$RUNS_DIR/run-${run_id}-${task_id}"

    log "═══════════════════════════════════════════════════"
    log "Executing Task: $task_id (Iteration $iteration)"
    log "Run Folder: $run_folder"
    log "═══════════════════════════════════════════════════"

    # Create run folder
    mkdir -p "$run_folder"

    # Initialize documentation
    cat > "$run_folder/THOUGHTS.md" << EOF
# THOUGHTS - $task_id

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Run:** $run_id

## Reasoning

EOF

    cat > "$run_folder/DECISIONS.md" << EOF
# DECISIONS - $task_id

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Decisions Made

EOF

    cat > "$run_folder/LEARNINGS.md" << EOF
# LEARNINGS - $task_id

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## What Worked Well

## What Was Harder Than Expected

## What Would We Do Differently

EOF

    cat > "$run_folder/RESULTS.md" << EOF
# RESULTS - $task_id

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status:** IN_PROGRESS

## Outcomes

EOF

    # Build and save prompt
    local prompt=$(build_prompt "$task_file" "$run_folder")
    echo "$prompt" > "$run_folder/prompt.md"

    # Execute with retries
    local retry_count=0
    local tmpfile="$run_folder/claude_output.log"

    while [ $retry_count -lt $MAX_RETRIES ]; do
        if [ $retry_count -gt 0 ]; then
            log_warn "Retry $retry_count/$MAX_RETRIES..."
            sleep $RETRY_DELAY
        fi

        if run_claude "$prompt" "$tmpfile"; then
            log_success "Claude execution completed"

            # Check for completion signal
            if grep -q "<promise>COMPLETE</promise>" "$tmpfile"; then
                log_success "Task signaled COMPLETE"
                echo "COMPLETED" > "$run_folder/status.txt"
                return 0
            elif grep -q "<promise>PARTIAL</promise>" "$tmpfile"; then
                log_warn "Task signaled PARTIAL"
                echo "PARTIAL" > "$run_folder/status.txt"
                return 1
            else
                log_warn "No completion signal found"
                echo "PARTIAL" > "$run_folder/status.txt"
                return 1
            fi
        else
            log_error "Claude execution failed (exit code: $?)"
            retry_count=$((retry_count + 1))
        fi
    done

    log_error "Task failed after $MAX_RETRIES attempts"
    echo "FAILED" > "$run_folder/status.txt"
    return 1
}

# Commit and push changes
commit_and_push() {
    local task_id="$1"
    local status="$2"

    cd "$BB5_DIR"

    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        log "Committing changes..."
        git add -A
        git commit -m "ralf-core: [$task_id] $status" 2>&1 | tee -a "$LOG_FILE" || true

        log "Pushing to GitHub..."
        if git push origin vps 2>&1 | tee -a "$LOG_FILE"; then
            log_success "Changes pushed to vps branch"
        else
            log_warn "Push failed, will retry next cycle"
        fi
    else
        log "No changes to commit"
    fi
}

# Main execution loop
main() {
    log "═══════════════════════════════════════════════════"
    log "RALF-Core Starting"
    log "═══════════════════════════════════════════════════"
    log "AI Provider: $AI_PROVIDER"
    log "Tasks Directory: $TASKS_DIR"
    log "Runs Directory: $RUNS_DIR"

    if [ "$AI_PROVIDER" = "none" ]; then
        log_error "No AI provider found (Claude or GLM required)"
        exit 1
    fi

    local iteration=0

    while true; do
        iteration=$((iteration + 1))

        log ""
        log "═══════════════════════════════════════════════════"
        log "Iteration $iteration"
        log "═══════════════════════════════════════════════════"

        # Pull latest changes
        log "Pulling latest from GitHub..."
        cd "$BB5_DIR"
        if git pull origin vps 2>&1 | tee -a "$LOG_FILE"; then
            log_success "Git pull complete"
        else
            log_warn "Git pull failed, continuing with local state"
        fi

        # Find next task
        local task_file=$(find_next_task)

        if [ -z "$task_file" ]; then
            log_success "No more pending/partial tasks found!"
            log "All tasks complete. Exiting."
            exit 0
        fi

        local task_id=$(basename "$task_file" .md)
        local remaining=$(count_remaining_tasks)
        log "Found task: $task_id ($remaining tasks remaining)"

        # Execute the task
        if execute_task "$task_file" "$iteration"; then
            log_success "Task $task_id completed successfully"
            commit_and_push "$task_id" "COMPLETED"
        else
            log_warn "Task $task_id completed partially or failed"
            commit_and_push "$task_id" "PARTIAL"
        fi

        # Brief pause before next iteration
        log "Sleeping before next iteration..."
        sleep 5
    done
}

# Run main loop
main "$@"
