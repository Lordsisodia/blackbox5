#!/bin/bash
# BB5 Simple Autonomous Improver
# Lightweight version that creates improvement tasks for agents

set -e

# Source common library for shared functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/bb5-common.sh"

# Initialize
BB5_SCRIPT_NAME="BB5-IMPROVER"
bb5_init_logging "bb5-simple-improver"
bb5_ensure_directories

# Alias bb5_log for backward compatibility
log() {
    bb5_log "$1"
}

log "═══════════════════════════════════════════════════"
log "BB5 Simple Improver Starting"
log "═══════════════════════════════════════════════════"

LOOP_COUNT=0
while true; do
    LOOP_COUNT=$((LOOP_COUNT + 1))
    RUN_ID=$(date +"%Y%m%d_%H%M%S")
    RUN_FOLDER="$RUNS_DIR/run-${RUN_ID}"
    mkdir -p "$RUN_FOLDER"

    log ""
    log "Cycle $LOOP_COUNT - Run $RUN_ID"

    # Pull latest
    bb5_git_pull "$RUN_FOLDER/git.log" || log "Pull failed"

    # Analyze BB5 state using common library functions
    ACTIVE_TASKS=$(bb5_count_active_tasks)
    RECENT_RUNS=$(ls -1t "$BB5_RUNS_DIR" 2>/dev/null | head -10 | wc -l)

    log "Active tasks: $ACTIVE_TASKS, Recent runs: $RECENT_RUNS"

    # Create improvement task based on state
    IMPROVEMENT_ID="IMP-$(date +%Y%m%d-%H%M%S)"
    IMPROVEMENT_FILE="$IMPROVEMENTS_DIR/${IMPROVEMENT_ID}.md"

    # Determine improvement type based on cycle
    case $((LOOP_COUNT % 5)) in
        1)
            IMPROVEMENT_TYPE="documentation"
            IMPROVEMENT_TITLE="Improve BB5 Documentation"
            IMPROVEMENT_DESC="Review and improve documentation in 1-docs/ and README files"
            ;;
        2)
            IMPROVEMENT_TYPE="agent"
            IMPROVEMENT_TITLE="Enhance Agent Definitions"
            IMPROVEMENT_DESC="Review .claude/agents/ and improve agent effectiveness"
            ;;
        3)
            IMPROVEMENT_TYPE="infrastructure"
            IMPROVEMENT_TITLE="Optimize BB5 Infrastructure"
            IMPROVEMENT_DESC="Review 2-engine/ and bin/ for optimization opportunities"
            ;;
        4)
            IMPROVEMENT_TYPE="memory"
            IMPROVEMENT_TITLE="Improve Project Memory"
            IMPROVEMENT_DESC="Organize and improve 5-project-memory/ structure"
            ;;
        0)
            IMPROVEMENT_TYPE="automation"
            IMPROVEMENT_TITLE="Enhance Automation"
            IMPROVEMENT_DESC="Improve hooks, loops, and autonomous processes"
            ;;
    esac

    # Create improvement task
    cat > "$IMPROVEMENT_FILE" << EOF
# Improvement Task: $IMPROVEMENT_TITLE

**ID:** $IMPROVEMENT_ID
**Type:** $IMPROVEMENT_TYPE
**Created:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Cycle:** $LOOP_COUNT

## Description
$IMPROVEMENT_DESC

## Context
- Active tasks: $ACTIVE_TASKS
- Recent runs: $RECENT_RUNS
- Run folder: $RUN_FOLDER

## Instructions
1. Analyze current state of $IMPROVEMENT_TYPE
2. Identify specific improvements
3. Implement changes
4. Test if applicable
5. Document what was done

## Success Criteria
- [ ] Analysis complete
- [ ] Improvements implemented
- [ ] Changes committed
- [ ] Documentation updated

## Notes
Created by BB5 Simple Improver cycle $LOOP_COUNT
EOF

    log "Created improvement task: $IMPROVEMENT_ID ($IMPROVEMENT_TYPE)"

    # Create run record
    cat > "$RUN_FOLDER/RESULTS.md" << EOF
# BB5 Simple Improver - Run $RUN_ID

**Cycle:** $LOOP_COUNT
**Status:** COMPLETED
**Improvement:** $IMPROVEMENT_ID

## Action
Created improvement task for $IMPROVEMENT_TYPE

## Next Steps
1. Process improvement task: $IMPROVEMENT_FILE
2. Implement changes
3. Mark as complete
EOF

    echo "COMPLETED" > "$RUN_FOLDER/status.txt"

    # Commit changes
    git add -A
    git commit -m "bb5-improver: [$RUN_ID] Created $IMPROVEMENT_TYPE improvement task" || true

    # Push
    git push origin vps 2>&1 | tee -a "$RUN_FOLDER/git.log" || log "Push failed"

    log "Cycle $LOOP_COUNT complete. Next cycle in 5 minutes..."

    # Sleep 5 minutes
    sleep 300
done
