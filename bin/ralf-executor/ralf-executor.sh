#!/bin/bash
# RALF Executor - Unified BB5 Task Execution Service
# Integrates task scanner, executor engine, and agent spawner
# Designed for VPS deployment with GLM/Claude AI provider

set -e

BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
EXECUTOR_DIR="$BB5_DIR/bin/ralf-executor"
TASKS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/tasks"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"
QUEUE_FILE="$BB5_DIR/5-project-memory/blackbox5/.autonomous/communications/queue-core.yaml"
LOG_FILE="$BB5_DIR/.autonomous/logs/ralf-executor.log"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} [RALF-EXECUTOR] $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} [RALF-EXECUTOR] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')]${NC} [RALF-EXECUTOR] $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')]${NC} [RALF-EXECUTOR] $1" | tee -a "$LOG_FILE"
}

# Initialize
mkdir -p "$TASKS_DIR/active" "$TASKS_DIR/completed" "$RUNS_DIR" "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$QUEUE_FILE")"

log "═══════════════════════════════════════════════════"
log "RALF Executor Starting"
log "═══════════════════════════════════════════════════"

# Detect AI provider
if [ -n "$ANTHROPIC_API_KEY" ] && command -v claude &> /dev/null; then
    AI_PROVIDER="claude"
    log "✓ Using Claude Code with GLM API"
elif command -v glm &> /dev/null; then
    AI_PROVIDER="glm"
    log "✓ Using GLM-4.7"
else
    AI_PROVIDER="none"
    log_warn "⚠ No AI provider detected - will create manual action items"
fi

# Main execution loop
CYCLE=0
while true; do
    CYCLE=$((CYCLE + 1))
    RUN_ID=$(date +"%Y%m%d_%H%M%S")
    RUN_FOLDER="$RUNS_DIR/run-${RUN_ID}"

    log ""
    log "═══════════════════════════════════════════════════"
    log "Execution Cycle $CYCLE - Run $RUN_ID"
    log "═══════════════════════════════════════════════════"

    # 1. Pull latest changes
    log "Pulling latest from GitHub..."
    cd "$BB5_DIR"
    if git pull origin vps 2>&1 | tee -a "$RUN_FOLDER/git.log" 2>/dev/null; then
        log_success "✓ Git pull complete"
    else
        log_warn "⚠ Git pull failed, continuing with local state"
    fi

    # 2. Scan for tasks and update queue
    log "Scanning for active tasks..."
    if [ -f "$EXECUTOR_DIR/task-scanner.py" ]; then
        python3 "$EXECUTOR_DIR/task-scanner.py" --tasks-dir "$TASKS_DIR/active" --queue "$QUEUE_FILE" --output "$RUN_FOLDER/scan-results.json" 2>&1 | tee -a "$LOG_FILE"
        log_success "✓ Task scan complete"
    else
        log_warn "⚠ Task scanner not found, using fallback"
        # Fallback: simple task detection
        PENDING_TASK=$(ls -1t "$TASKS_DIR/active"/*.md 2>/dev/null | head -1 || true)
        if [ -n "$PENDING_TASK" ]; then
            TASK_NAME=$(basename "$PENDING_TASK" .md)
            log "Found task: $TASK_NAME"
        fi
    fi

    # 3. Check if there are tasks to execute
    PENDING_COUNT=$(ls -1 "$TASKS_DIR/active"/*.md 2>/dev/null | wc -l)
    log "Pending tasks: $PENDING_COUNT"

    if [ "$PENDING_COUNT" -eq 0 ]; then
        log "No pending tasks. Checking for improvements..."
        # Could trigger improvement generation here
        log "Sleeping before next cycle..."
        sleep 60
        continue
    fi

    # 4. Execute the highest priority task
    log "Executing highest priority task..."

    if [ -f "$EXECUTOR_DIR/executor.py" ] && [ "$AI_PROVIDER" != "none" ]; then
        # Use the Python executor with AI
        export BB5_DIR
        export AI_PROVIDER
        export ANTHROPIC_API_KEY
        export ANTHROPIC_BASE_URL="https://api.glm.ai/coding/"

        if python3 "$EXECUTOR_DIR/executor.py" --run-folder "$RUN_FOLDER" --tasks-dir "$TASKS_DIR" 2>&1 | tee -a "$LOG_FILE"; then
            log_success "✓ Task execution completed"
        else
            log_error "❌ Task execution failed"
        fi
    else
        # Manual mode - create action items
        log_warn "Running in manual mode (no AI provider)"

        PENDING_TASK=$(ls -1t "$TASKS_DIR/active"/*.md 2>/dev/null | head -1)
        if [ -n "$PENDING_TASK" ]; then
            TASK_NAME=$(basename "$PENDING_TASK" .md)

            mkdir -p "$RUN_FOLDER"
            cat > "$RUN_FOLDER/THOUGHTS.md" << EOF
# RALF Executor - Manual Mode

**Run:** $RUN_ID
**Task:** $TASK_NAME
**Status:** PENDING_MANUAL_EXECUTION

## Action Required

No AI provider configured. Task requires manual execution:

1. Review task: $PENDING_TASK
2. Execute the improvements described
3. Move task to completed: $TASKS_DIR/completed/
4. Update this run folder with results

## To Enable AI Execution

Install GLM:
  curl -fsSL https://glm.ai/install.sh | sh

Or configure Claude with ANTHROPIC_API_KEY
EOF

            echo "PENDING" > "$RUN_FOLDER/status.txt"
            log "Created manual action item in $RUN_FOLDER"
        fi
    fi

    # 5. Commit and push changes
    log "Checking for changes to commit..."
    cd "$BB5_DIR"

    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        git add -A
        git commit -m "ralf-executor: [$RUN_ID] execution cycle $CYCLE" 2>&1 | tee -a "$RUN_FOLDER/git.log" || true
        log_success "✓ Changes committed"

        if git push origin vps 2>&1 | tee -a "$RUN_FOLDER/git.log"; then
            log_success "✓ Pushed to GitHub (vps branch)"
        else
            log_warn "⚠ Push failed (will retry next cycle)"
        fi
    else
        log "No changes to commit"
    fi

    # 6. Cycle complete
    log ""
    log "═══════════════════════════════════════════════════"
    log "Cycle $CYCLE Complete"
    log "═══════════════════════════════════════════════════"

    # Sleep before next cycle
    log "Sleeping for 5 minutes..."
    sleep 300
done
