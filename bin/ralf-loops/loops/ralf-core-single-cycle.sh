#!/bin/bash
# RALF-CORE Single Cycle: Run agent teams, log everything, then exit
# Designed for Moltbot management - runs once, completes, then Moltbot restarts

set -e

RALF_TYPE="core"
BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
PROMPT_FILE="$BB5_DIR/bin/ralf-loops/prompts/ralf-core.md"
QUEUE_FILE="$BB5_DIR/5-project-memory/blackbox5/.autonomous/communications/queue-core.yaml"
STATE_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/state"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"

# Single run - no loop
RUN_ID=$(date +"%Y%m%d_%H%M%S")
RUN_FOLDER="$RUNS_DIR/run-${RUN_ID}"

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

log_warn() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')]${NC} [RALF-CORE] $1"
}

# Initialize
log "═══════════════════════════════════════════════════"
log "RALF-CORE Single Cycle - Agent Teams Mode"
log "═══════════════════════════════════════════════════"
log "Run ID: $RUN_ID"
log "Run Folder: $RUN_FOLDER"
log ""

# Ensure directories exist
mkdir -p "$RUN_FOLDER" "$STATE_DIR"
mkdir -p "$(dirname "$QUEUE_FILE")"

# 1. CHECK PREVIOUS RUN CONTEXT
log "Checking previous runs for context..."
PREVIOUS_RUN=$(ls -1t "$RUNS_DIR" 2>/dev/null | grep -v "^run-${RUN_ID}$" | head -1)
if [ -n "$PREVIOUS_RUN" ] && [ -f "$RUNS_DIR/$PREVIOUS_RUN/status.txt" ]; then
    PREVIOUS_STATUS=$(cat "$RUNS_DIR/$PREVIOUS_RUN/status.txt" 2>/dev/null || echo "UNKNOWN")
    log "Previous run: $PREVIOUS_RUN (status: $PREVIOUS_STATUS)"
    echo "previous_run: $PREVIOUS_RUN" >> "$RUN_FOLDER/context.yaml"
    echo "previous_status: $PREVIOUS_STATUS" >> "$RUN_FOLDER/context.yaml"
else
    log "No previous runs found"
    echo "previous_run: none" >> "$RUN_FOLDER/context.yaml"
fi

# 2. PULL LATEST
log "Pulling latest from GitHub..."
cd "$BB5_DIR"
if git pull origin main 2>&1 | tee -a "$RUN_FOLDER/git.log"; then
    log_success "Git pull complete"
    GIT_CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
    log "Uncommitted changes: $GIT_CHANGES"
else
    log_warn "Git pull failed, continuing with local state"
fi

# 3. ANALYZE BB5 STATE
log "Analyzing BB5 state..."

# Check for active tasks
ACTIVE_TASKS=$(find "$BB5_DIR/.autonomous/tasks/active" -name "*.md" 2>/dev/null | wc -l)
log "Active tasks: $ACTIVE_TASKS"

# Check recent runs
RECENT_RUNS=$(ls -1t "$RUNS_DIR" 2>/dev/null | head -5 | wc -l)
log "Recent runs: $RECENT_RUNS"

# Check goals
if [ -f "$BB5_DIR/goals.yaml" ]; then
    GOALS_STATUS=$(grep "^  - id:" "$BB5_DIR/goals.yaml" 2>/dev/null | wc -l)
    log "Goals defined: $GOALS_STATUS"
fi

# 4. DETERMINE NEXT ACTION
log "Determining next action based on state..."

# Priority logic
if [ "$ACTIVE_TASKS" -gt 0 ]; then
    ACTION="process_active_tasks"
    PRIORITY="high"
    log "Action: Process $ACTIVE_TASKS active tasks"
elif [ -n "$PREVIOUS_RUN" ] && [ "$PREVIOUS_STATUS" = "PARTIAL" ]; then
    ACTION="continue_previous"
    PRIORITY="high"
    log "Action: Continue previous partial run"
elif [ "$GIT_CHANGES" -gt 0 ]; then
    ACTION="commit_changes"
    PRIORITY="medium"
    log "Action: Commit $GIT_CHANGES pending changes"
else
    ACTION="analyze_improve"
    PRIORITY="medium"
    log "Action: Analyze for improvements"
fi

# 5. CREATE RUN DOCUMENTATION
cat > "$RUN_FOLDER/context.yaml" << EOF
run:
  id: $RUN_ID
  type: ralf-core
  action: $ACTION
  priority: $PRIORITY
  previous_run: ${PREVIOUS_RUN:-none}
  previous_status: ${PREVIOUS_STATUS:-none}
  active_tasks: $ACTIVE_TASKS
  git_changes: ${GIT_CHANGES:-0}
started: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

cat > "$RUN_FOLDER/THOUGHTS.md" << EOF
# RALF-CORE Run $RUN_ID - THOUGHTS

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Action:** $ACTION
**Priority:** $PRIORITY

## Context from Previous Run
${PREVIOUS_RUN:+- Previous: $PREVIOUS_RUN (status: $PREVIOUS_STATUS)}
${PREVIOUS_RUN:-- No previous run}

## Current State
- Active tasks: $ACTIVE_TASKS
- Git changes: ${GIT_CHANGES:-0}
- Recent runs: $RECENT_RUNS

## Plan
1. Activate BB5 Core Agent Team
2. Execute: $ACTION
3. Log all decisions and learnings
4. Complete and exit

## Execution Log

EOF

cat > "$RUN_FOLDER/DECISIONS.md" << EOF
# RALF-CORE Run $RUN_ID - DECISIONS

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Cycle Decision
**Decision:** Execute $ACTION
**Rationale:** Based on BB5 state analysis
**Priority:** $PRIORITY

EOF

cat > "$RUN_FOLDER/LEARNINGS.md" << EOF
# RALF-CORE Run $RUN_ID - LEARNINGS

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## What Worked Well

## What Was Harder Than Expected

## What Would We Do Differently

## Patterns Detected

EOF

cat > "$RUN_FOLDER/RESULTS.md" << EOF
# RALF-CORE Run $RUN_ID - RESULTS

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status:** IN_PROGRESS

## Action Executed
$ACTION

## Outcomes

## Next Steps

EOF

# 6. ACTIVATE BB5 CORE AGENT TEAM
log "═══════════════════════════════════════════════════"
log "Activating BB5 Core Agent Team..."
log "═══════════════════════════════════════════════════"

# Create agent team activation marker
cat > "$RUN_FOLDER/.agent_teams_active" << EOF
AGENT_TEAMS_ACTIVE: true
RUN_ID: $RUN_ID
ACTIVATED_AT: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
CORE_TEAM:
  - bb5-context-collector: Gather BB5 state
  - bb5-superintelligence: Analyze and decide
  - bb5-scribe: Document everything
ACTION: $ACTION
EOF

log "Agent team activation created"
log "  - Context Collector: Will gather state"
log "  - Superintelligence: Will analyze $ACTION"
log "  - Scribe: Will document to run folder"

# 7. EXECUTE WITH AGENT TEAMS
log ""
log "Executing with Agent Teams..."
log "This will spawn sub-agents to complete: $ACTION"
log ""

# Detect which AI to use
if command -v glm &> /dev/null; then
    AI_PROVIDER="glm"
    AI_CMD="glm"
    log "GLM-4.7 detected, using GLM for agent teams"
elif [ -n "$ANTHROPIC_API_KEY" ] || [ -f "$HOME/.config/claude/config.json" ]; then
    AI_PROVIDER="claude"
    log "Claude API configured, spawning agent teams..."
else
    AI_PROVIDER="none"
    log_warn "No AI provider detected (GLM or Claude)"
fi

if [ "$AI_PROVIDER" != "none" ]; then
    # Create the execution prompt
    cat > "$RUN_FOLDER/execution-prompt.md" << EOF
You are the BB5 Core Agent Team Coordinator for run $RUN_ID.

## Mission
Execute the action: $ACTION
Priority: $PRIORITY

## Context
- Run folder: $RUN_FOLDER
- Active tasks: $ACTIVE_TASKS
- Previous run: ${PREVIOUS_RUN:-none} (${PREVIOUS_STATUS:-none})

## Agent Team
1. **bb5-context-collector**: First, gather current BB5 state
   - Read .autonomous/tasks/active/
   - Check goals.yaml
   - Review previous run if exists
   - Write findings to CONTEXT_REPORT.md

2. **bb5-superintelligence**: Then analyze and decide
   - Use context report
   - Perform 7-dimension analysis if needed
   - Make decision on $ACTION
   - Write to SUPERINTELLIGENCE_ANALYSIS.md

3. **bb5-scribe**: Continuously document
   - Update THOUGHTS.md with reasoning
   - Log DECISIONS.md
   - Capture LEARNINGS.md

## Output
All outputs go to: $RUN_FOLDER/

## Completion
When done, update $RUN_FOLDER/status.txt with: COMPLETED, PARTIAL, or FAILED
And update RESULTS.md with outcomes.
EOF

    # Execute with appropriate AI
    export RALF_TASK_ID="CORE-$RUN_ID"
    export RALF_RUN_FOLDER="$RUN_FOLDER"

    if [ "$AI_PROVIDER" = "glm" ]; then
        log "Spawning GLM-4.7 with agent teams..."
        if glm chat --model 4.7 --system "You are BB5 Core Agent Team Coordinator" < "$RUN_FOLDER/execution-prompt.md" 2>&1 | tee "$RUN_FOLDER/ralf-output.log"; then
            log_success "GLM execution completed"
        else
            log_error "GLM execution failed"
            echo "FAILED" > "$RUN_FOLDER/status.txt"
        fi
    elif [ "$AI_PROVIDER" = "claude" ]; then
        # Skip --dangerously-skip-permissions when running as root
        if [ "$(id -u)" -eq 0 ]; then
            CLAUDE_CMD="claude -p"
        else
            CLAUDE_CMD="claude -p --dangerously-skip-permissions"
        fi

        log "Spawning Claude Code with agent teams..."
        if $CLAUDE_CMD < "$RUN_FOLDER/execution-prompt.md" 2>&1 | tee "$RUN_FOLDER/ralf-output.log"; then
            log_success "Claude execution completed"
        else
            log_error "Claude execution failed"
            echo "FAILED" > "$RUN_FOLDER/status.txt"
        fi
    fi
else
    log_warn "No AI provider configured"
    log "Creating manual action items..."

    cat >> "$RUN_FOLDER/THOUGHTS.md" << EOF

## $(date '+%H:%M:%S') - Manual Action Required
No AI provider configured (GLM or Claude). Cannot spawn agent teams automatically.

Action required: $ACTION
Priority: $PRIORITY

To complete manually:
1. Review active tasks in .autonomous/tasks/active/
2. Check previous run: ${PREVIOUS_RUN:-none}
3. Execute: $ACTION
4. Update this run folder with results

To enable agent teams, install GLM:
  curl -fsSL https://glm.ai/install.sh | sh

Or set ANTHROPIC_API_KEY for Claude

EOF

    echo "PENDING" > "$RUN_FOLDER/status.txt"
fi

# 8. CHECK COMPLETION STATUS
if [ -f "$RUN_FOLDER/status.txt" ]; then
    FINAL_STATUS=$(cat "$RUN_FOLDER/status.txt")
else
    FINAL_STATUS="PARTIAL"
    echo "$FINAL_STATUS" > "$RUN_FOLDER/status.txt"
fi

log "Run status: $FINAL_STATUS"

# 9. COMMIT CHANGES
log "Checking for changes to commit..."
cd "$BB5_DIR"

if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    git add -A
    git commit -m "ralf-core: [$RUN_ID] $ACTION - $FINAL_STATUS" 2>&1 | tee -a "$RUN_FOLDER/git.log" || true
    log_success "Changes committed"

    # Try to push
    if git push origin main 2>&1 | tee -a "$RUN_FOLDER/git.log"; then
        log_success "Pushed to GitHub"
    else
        log_warn "Push failed (will retry next cycle)"
    fi
else
    log "No changes to commit"
fi

# 10. FINALIZE
log ""
log "═══════════════════════════════════════════════════"
log "RALF-CORE Cycle Complete"
log "═══════════════════════════════════════════════════"
log "Run ID: $RUN_ID"
log "Status: $FINAL_STATUS"
log "Action: $ACTION"
log "Run folder: $RUN_FOLDER"
log ""
log "Moltbot should now:"
log "  1. Read $RUN_FOLDER/RESULTS.md"
log "  2. Check status: $FINAL_STATUS"
log "  3. Decide next action"
log "  4. Restart RALF-CORE if needed"
log "═══════════════════════════════════════════════════"

# Exit with status for Moltbot
if [ "$FINAL_STATUS" = "COMPLETED" ]; then
    exit 0
elif [ "$FINAL_STATUS" = "FAILED" ]; then
    exit 1
else
    exit 2  # PARTIAL - needs continuation
fi
