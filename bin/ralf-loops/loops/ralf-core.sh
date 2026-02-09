#!/bin/bash
# RALF-CORE: Engine Improvement Loop
# Runs continuously, improving BlackBox5 engine

set -e

RALF_TYPE="core"
BB5_DIR="/opt/blackbox5"
PROMPT_FILE="$BB5_DIR/bin/ralf-loops/prompts/ralf-core.md"
QUEUE_FILE="$BB5_DIR/5-project-memory/blackbox5/.autonomous/communications/queue-core.yaml"
STATE_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/state"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1"
}

# Initialize
log "Starting RALF-CORE loop..."
log "Working directory: $BB5_DIR"
log "Prompt: $PROMPT_FILE"

# Ensure directories exist
mkdir -p "$STATE_DIR" "$RUNS_DIR"
mkdir -p "$(dirname "$QUEUE_FILE")"

# Create queue file if not exists
if [ ! -f "$QUEUE_FILE" ]; then
    cat > "$QUEUE_FILE" << 'EOF'
queue:
  - task_id: "INIT-001"
    description: "Analyze 2-engine/ for improvement opportunities"
    priority: high
    status: pending
    created: "2026-02-09T00:00:00Z"
EOF
fi

LOOP_COUNT=0

while true; do
    LOOP_COUNT=$((LOOP_COUNT + 1))
    echo ""
    log "=== LOOP $LOOP_COUNT ==="

    # Check if paused
    if [ -f "$BB5_DIR/.paused-core" ]; then
        log "Paused. Sleeping 30s..."
        sleep 30
        continue
    fi

    # 1. PULL LATEST
    log "Pulling latest from GitHub..."
    cd "$BB5_DIR"
    git pull origin main 2>/dev/null || log "Pull failed, continuing..."

    # 2. CHECK FOR PENDING TASKS
    log "Checking for pending tasks..."

    # Read queue and find pending task
    PENDING_TASK=$(python3 -c "
import yaml
try:
    with open('$QUEUE_FILE', 'r') as f:
        data = yaml.safe_load(f) or {}
    queue = data.get('queue', [])
    for task in queue:
        if task.get('status') == 'pending':
            print(task.get('task_id', 'UNKNOWN'))
            break
except Exception as e:
    print('ERROR')
" 2>/dev/null)

    if [ "$PENDING_TASK" = "ERROR" ] || [ -z "$PENDING_TASK" ]; then
        log "No pending tasks. Creating analysis task..."

        # Create new analysis task
        TASK_ID="CORE-$(date +%Y%m%d-%H%M%S)"
        python3 -c "
import yaml
from datetime import datetime

try:
    with open('$QUEUE_FILE', 'r') as f:
        data = yaml.safe_load(f) or {'queue': []}

    new_task = {
        'task_id': '$TASK_ID',
        'description': 'Analyze 2-engine/ for improvement opportunities',
        'priority': 'medium',
        'status': 'pending',
        'created': datetime.now().isoformat()
    }
    data['queue'].append(new_task)

    with open('$QUEUE_FILE', 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    print('CREATED')
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null

        log "Created task $TASK_ID"
        sleep 5
        continue
    fi

    log "Found pending task: $PENDING_TASK"

    # 3. CREATE RUN FOLDER
    RUN_ID="run-$(date +%Y%m%d_%H%M%S)"
    RUN_FOLDER="$RUNS_DIR/$RUN_ID"
    mkdir -p "$RUN_FOLDER"
    log "Created run folder: $RUN_FOLDER"

    # Initialize run documentation
    cat > "$RUN_FOLDER/THOUGHTS.md" << EOF
# THOUGHTS - RALF-CORE Loop $LOOP_COUNT

**Task:** $PENDING_TASK
**Started:** $(date)
**Run:** $RUN_ID

## Initial Assessment

Analyzing 2-engine/ for improvement opportunities...

EOF

    cat > "$RUN_FOLDER/DECISIONS.md" << EOF
# DECISIONS - RALF-CORE Loop $LOOP_COUNT

**Task:** $PENDING_TASK
**Started:** $(date)

## Decisions Made

EOF

    cat > "$RUN_FOLDER/LEARNINGS.md" << EOF
# LEARNINGS - RALF-CORE Loop $LOOP_COUNT

**Task:** $PENDING_TASK
**Started:** $(date)

## What I Learned

EOF

    cat > "$RUN_FOLDER/RESULTS.md" << EOF
# RESULTS - RALF-CORE Loop $LOOP_COUNT

**Task:** $PENDING_TASK
**Status:** in_progress
**Started:** $(date)

## Outcome

EOF

    # 4. UPDATE TASK STATUS
    python3 -c "
import yaml
from datetime import datetime

try:
    with open('$QUEUE_FILE', 'r') as f:
        data = yaml.safe_load(f) or {'queue': []}

    for task in data['queue']:
        if task.get('task_id') == '$PENDING_TASK':
            task['status'] = 'in_progress'
            task['started'] = datetime.now().isoformat()
            task['run_folder'] = '$RUN_FOLDER'
            break

    with open('$QUEUE_FILE', 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null

    # 5. RUN RALF WITH PROMPT
    log "Executing RALF-CORE..."

    # Create context file for the prompt
    cat > "$RUN_FOLDER/context.yaml" << EOF
ralf_context:
  type: core
  task_id: $PENDING_TASK
  run_folder: $RUN_FOLDER
  loop_count: $LOOP_COUNT
  queue_file: $QUEUE_FILE
EOF

    # Execute Claude Code with the prompt
    export RALF_TASK_ID="$PENDING_TASK"
    export RALF_RUN_FOLDER="$RUN_FOLDER"
    export RALF_LOOP_COUNT="$LOOP_COUNT"

    # Skip --dangerously-skip-permissions when running as root (VPS)
    if [ "$(id -u)" -eq 0 ]; then
        CLAUDE_CMD="claude -p"
    else
        CLAUDE_CMD="claude -p --dangerously-skip-permissions"
    fi

    if ! $CLAUDE_CMD < "$PROMPT_FILE" 2>&1 | tee "$RUN_FOLDER/ralf-output.log"; then
        log_error "RALF execution failed"
        echo "FAILED" > "$RUN_FOLDER/status.txt"

        # Update task as failed
        python3 -c "
import yaml
from datetime import datetime

try:
    with open('$QUEUE_FILE', 'r') as f:
        data = yaml.safe_load(f) or {'queue': []}

    for task in data['queue']:
        if task.get('task_id') == '$PENDING_TASK':
            task['status'] = 'failed'
            task['completed'] = datetime.now().isoformat()
            break

    with open('$QUEUE_FILE', 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
except Exception as e:
    pass
" 2>/dev/null

        sleep 30
        continue
    fi

    # 6. CHECK FOR COMPLETION SIGNAL
    if grep -q "<promise>COMPLETE</promise>" "$RUN_FOLDER/ralf-output.log" 2>/dev/null; then
        log_success "Task completed successfully"
        echo "COMPLETED" > "$RUN_FOLDER/status.txt"

        # Update task as completed
        python3 -c "
import yaml
from datetime import datetime

try:
    with open('$QUEUE_FILE', 'r') as f:
        data = yaml.safe_load(f) or {'queue': []}

    for task in data['queue']:
        if task.get('task_id') == '$PENDING_TASK':
            task['status'] = 'completed'
            task['completed'] = datetime.now().isoformat()
            break

    with open('$QUEUE_FILE', 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
except Exception as e:
    pass
" 2>/dev/null

    else
        log "Task did not signal completion. Marking as partial..."
        echo "PARTIAL" > "$RUN_FOLDER/status.txt"

        # Update task as partial
        python3 -c "
import yaml
from datetime import datetime

try:
    with open('$QUEUE_FILE', 'r') as f:
        data = yaml.safe_load(f) or {'queue': []}

    for task in data['queue']:
        if task.get('task_id') == '$PENDING_TASK':
            task['status'] = 'partial'
            task['completed'] = datetime.now().isoformat()
            break

    with open('$QUEUE_FILE', 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
except Exception as e:
    pass
" 2>/dev/null
    fi

    # 7. COMMIT CHANGES
    log "Checking for changes..."
    cd "$BB5_DIR"

    if ! git diff --quiet HEAD 2>/dev/null || ! git diff --cached --quiet HEAD 2>/dev/null; then
        log "Changes detected. Committing..."

        git add -A
        git commit -m "ralf-core: [$RUN_ID] $PENDING_TASK

- Autonomous engine improvement
- Run: $RUN_ID
- Status: $(cat $RUN_FOLDER/status.txt 2>/dev/null || echo 'unknown')

Auto-generated by RALF-CORE" || true

        log "Pushing to GitHub..."
        git push origin main 2>/dev/null || log_error "Push failed, will retry"
    else
        log "No changes to commit"
    fi

    # 8. BRIEF PAUSE
    log "Loop $LOOP_COUNT complete. Sleeping 10s..."
    echo ""
    sleep 10
done
