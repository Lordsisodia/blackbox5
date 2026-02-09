#!/bin/bash
# BB5 Autonomous Improver
# Uses superintelligence to analyze BB5 and decide what to improve
# Runs continuously on VPS with full agent teams

set -e

BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"
STATE_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/state"
LOG_FILE="$BB5_DIR/.autonomous/logs/bb5-improver.log"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} [BB5-IMPROVER] $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} [BB5-IMPROVER] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')]${NC} [BB5-IMPROVER] $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')]${NC} [BB5-IMPROVER] $1" | tee -a "$LOG_FILE"
}

# Ensure directories exist
mkdir -p "$RUNS_DIR" "$STATE_DIR" "$(dirname "$LOG_FILE")"

log "═══════════════════════════════════════════════════"
log "BB5 Autonomous Improver Starting"
log "═══════════════════════════════════════════════════"
log "BB5 Directory: $BB5_DIR"
log "Runs Directory: $RUNS_DIR"
log ""

# Check AI provider
if command -v claude &> /dev/null; then
    AI_PROVIDER="claude"
    log "✓ Claude Code detected"
elif command -v glm &> /dev/null; then
    AI_PROVIDER="glm"
    log "✓ GLM-4.7 detected"
else
    log_error "No AI provider found (Claude or GLM required)"
    exit 1
fi

# Main improvement loop
LOOP_COUNT=0
while true; do
    LOOP_COUNT=$((LOOP_COUNT + 1))
    RUN_ID=$(date +"%Y%m%d_%H%M%S")
    RUN_FOLDER="$RUNS_DIR/run-${RUN_ID}"
    mkdir -p "$RUN_FOLDER"

    log ""
    log "═══════════════════════════════════════════════════"
    log "Improvement Cycle $LOOP_COUNT - Run $RUN_ID"
    log "═══════════════════════════════════════════════════"

    # 1. PULL LATEST
    log "Pulling latest from GitHub..."
    cd "$BB5_DIR"
    git pull origin vps 2>&1 | tee -a "$RUN_FOLDER/git.log" || log_warn "Pull failed, continuing..."

    # 2. GATHER CONTEXT
    log "Gathering BB5 context..."

    # Count active tasks
    ACTIVE_TASKS=$(find "$BB5_DIR/5-project-memory/blackbox5/.autonomous/tasks/active" -name "*.md" 2>/dev/null | wc -l)
    log "  Active tasks: $ACTIVE_TASKS"

    # Check recent runs
    RECENT_RUNS=$(ls -1t "$RUNS_DIR" 2>/dev/null | head -5 | wc -l)
    log "  Recent runs: $RECENT_RUNS"

    # Check goals
    ACTIVE_GOALS=$(ls -1 "$BB5_DIR/5-project-memory/blackbox5/goals/active/" 2>/dev/null | wc -l)
    log "  Active goals: $ACTIVE_GOALS"

    # Check for improvements
    IMPROVEMENTS=$(ls -1 "$BB5_DIR/5-project-memory/blackbox5/.autonomous/tasks/improvements/" 2>/dev/null | wc -l)
    log "  Pending improvements: $IMPROVEMENTS"

    # 3. CREATE CONTEXT REPORT
    cat > "$RUN_FOLDER/CONTEXT_REPORT.md" << EOF
# BB5 Context Report - Run $RUN_ID

**Generated:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Cycle:** $LOOP_COUNT

## Current State

### Tasks
- Active tasks: $ACTIVE_TASKS
- Pending improvements: $IMPROVEMENTS

### Goals
- Active goals: $ACTIVE_GOALS

### Recent Activity
- Recent runs: $RECENT_RUNS
- Run folder: $RUN_FOLDER

## BB5 Infrastructure Overview

### Core Components
- \`2-engine/\` - Framework, workflows, tools, CLI
- \`5-project-memory/blackbox5/\` - Project memory and state
- \`.claude/agents/\` - Agent definitions
- \`.claude/skills/\` - Skill system
- \`bin/ralf-loops/\` - RALF improvement loops

### Agent Teams
- **bb5-context-collector**: Gathers BB5 state
- **bb5-superintelligence**: Performs 7-dimension analysis
- **bb5-scribe**: Documents everything

### Key Files
- \`5-project-memory/blackbox5/STATE.yaml\` - Goal tracking
- \`5-project-memory/blackbox5/timeline.yaml\` - Project timeline
- \`5-project-memory/blackbox5/.autonomous/agents/communications/spawn-queue.yaml\` - Agent queue

## What Needs Improvement?

This is what the superintelligence agent will analyze and decide.
EOF

    log "Context report created: $RUN_FOLDER/CONTEXT_REPORT.md"

    # 4. ACTIVATE SUPERINTELLIGENCE
    log ""
    log "═══════════════════════════════════════════════════"
    log "Activating BB5 Superintelligence Agent"
    log "═══════════════════════════════════════════════════"

    cat > "$RUN_FOLDER/superintelligence-prompt.md" << 'SUPERPROMPT'
You are the BB5 Superintelligence Agent. Analyze BlackBox5 and decide what to improve.

## Your Mission
1. Read the CONTEXT_REPORT.md
2. Analyze BB5 infrastructure for improvement opportunities
3. Use 7-dimension superintelligence protocol
4. Decide on ONE specific improvement to make
5. Execute that improvement

## 7-Dimension Analysis

### 1. First Principles
- What is BB5 fundamentally trying to achieve?
- What are the core constraints?
- What can be improved?

### 2. Information Gathering
- Review 2-engine/ for technical debt
- Check .autonomous/ for operational issues
- Look at recent runs for patterns

### 3. Multi-Perspective Analysis
- **Architect**: System design, scalability
- **Developer**: Code quality, maintainability
- **Operator**: Automation, reliability
- **User**: Usability, documentation

### 4. Temporal Reasoning
- Past: What improvements have worked?
- Present: What's the current pain point?
- Future: What will have the most impact?

### 5. Meta-Cognitive Check
- What are my assumptions?
- What could go wrong?
- Am I being too ambitious?

### 6. Recursive Refinement
- Break down the improvement into steps
- Identify dependencies
- Plan the execution

### 7. Synthesis
- Make a clear decision
- Define success criteria
- Plan the implementation

## Output Requirements

Create these files in the run folder:

1. **SUPERINTELLIGENCE_ANALYSIS.md** - Full analysis
2. **DECISIONS.md** - What was decided and why
3. **THOUGHTS.md** - Reasoning process
4. **IMPROVEMENT_PLAN.md** - Specific plan
5. **status.txt** - COMPLETED, PARTIAL, or FAILED

## Improvement Categories

Choose from:
- **Infrastructure** - Improve engine, workflows, tools
- **Agent System** - Enhance agent definitions, add new agents
- **Documentation** - Improve docs, add examples
- **Automation** - Add hooks, improve loops
- **Integration** - Connect with external systems
- **Performance** - Optimize speed, reduce overhead

## Constraints

- Make SMALL, focused improvements
- One improvement per cycle
- Must be completable in 30 minutes
- Must improve BB5's autonomous capability
- Must be safe (don't break existing functionality)

## Success Criteria

- Improvement is implemented
- Tests pass (if applicable)
- Documentation updated
- Changes committed to git
SUPERPROMPT

    # Add context to prompt
    cat "$RUN_FOLDER/CONTEXT_REPORT.md" >> "$RUN_FOLDER/superintelligence-prompt.md"

    # 5. EXECUTE WITH CLAUDE
    log "Executing superintelligence analysis with Claude..."

    export BB5_RUN_FOLDER="$RUN_FOLDER"
    export BB5_RUN_ID="$RUN_ID"
    export BB5_CYCLE="$LOOP_COUNT"

    if [ "$AI_PROVIDER" = "claude" ]; then
        # Run Claude with superintelligence prompt
        if claude -p < "$RUN_FOLDER/superintelligence-prompt.md" 2>&1 | tee "$RUN_FOLDER/execution.log"; then
            log_success "Claude execution completed"
        else
            log_error "Claude execution failed"
            echo "FAILED" > "$RUN_FOLDER/status.txt"
        fi
    elif [ "$AI_PROVIDER" = "glm" ]; then
        log "Using GLM-4.7 for execution..."
        if glm chat --model 4.7 < "$RUN_FOLDER/superintelligence-prompt.md" 2>&1 | tee "$RUN_FOLDER/execution.log"; then
            log_success "GLM execution completed"
        else
            log_error "GLM execution failed"
            echo "FAILED" > "$RUN_FOLDER/status.txt"
        fi
    fi

    # 6. CHECK STATUS
    if [ -f "$RUN_FOLDER/status.txt" ]; then
        FINAL_STATUS=$(cat "$RUN_FOLDER/status.txt")
    else
        FINAL_STATUS="PARTIAL"
        echo "$FINAL_STATUS" > "$RUN_FOLDER/status.txt"
    fi

    log "Run status: $FINAL_STATUS"

    # 7. COMMIT CHANGES
    log "Checking for changes..."
    cd "$BB5_DIR"

    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        git add -A
        git commit -m "bb5-improver: [$RUN_ID] Cycle $LOOP_COUNT - $FINAL_STATUS" 2>&1 | tee -a "$RUN_FOLDER/git.log" || true
        log_success "Changes committed"

        # Push to GitHub
        if git push origin vps 2>&1 | tee -a "$RUN_FOLDER/git.log"; then
            log_success "Pushed to GitHub"
        else
            log_warn "Push failed (will retry next cycle)"
        fi
    else
        log "No changes to commit"
    fi

    # 8. CYCLE COMPLETE
    log ""
    log "═══════════════════════════════════════════════════"
    log "Cycle $LOOP_COUNT Complete"
    log "═══════════════════════════════════════════════════"
    log "Run ID: $RUN_ID"
    log "Status: $FINAL_STATUS"
    log "Next cycle in 5 minutes..."
    log "═══════════════════════════════════════════════════"

    # Sleep before next cycle
    sleep 300  # 5 minutes

done
