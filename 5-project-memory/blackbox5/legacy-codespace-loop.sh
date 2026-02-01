#!/bin/bash
# Legacy Autonomous Loop - Proper RALF-based continuous improvement

set -e
cd /workspaces/blackbox5

export ANTHROPIC_API_KEY='455a01beaad94e00b91e8b99b2cb74f6.m0gimfbfc6AlitLz'
export ANTHROPIC_BASE_URL='https://api.z.ai/api/anthropic'

PROJECT_DIR=/workspaces/blackbox5/5-project-memory/blackbox5
ENGINE_DIR=/workspaces/blackbox5/2-engine/.autonomous
PROMPT_FILE=$ENGINE_DIR/prompts/ralf.md
LOG_DIR=$PROJECT_DIR/.autonomous/LOGS

mkdir -p $LOG_DIR

while true; do
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SESSION_LOG="$LOG_DIR/legacy-session-$TIMESTAMP.log"

    echo "═══════════════════════════════════════════════════════════"
    echo "  Legacy Agent Cycle - $TIMESTAMP"
    echo "  Branch: $(git branch --show-current)"
    echo "═══════════════════════════════════════════════════════════"

    # Pull latest changes
    git pull origin legacy/autonomous-improvement || true

    # Run RALF
    export RALF_PROJECT_DIR="$PROJECT_DIR"
    export RALF_ENGINE_DIR="$ENGINE_DIR"
    export RALF_BLACKBOX5_DIR="/workspaces/blackbox5"

    if claude -p --dangerously-skip-permissions < "$PROMPT_FILE" 2>&1 | tee -a "$SESSION_LOG"; then
        echo "RALF cycle completed"
    else
        echo "RALF cycle had issues, continuing..."
    fi

    # Push any commits
    git push origin legacy/autonomous-improvement 2>&1 || echo "Nothing to push"

    # Check if we should stop (COMPLETE signal found)
    if grep -q '<promise>COMPLETE</promise>' "$SESSION_LOG" 2>/dev/null; then
        echo "Task complete. Restarting in 60 seconds for next cycle..."
    else
        echo "Cycle ended. Continuing in 60 seconds..."
    fi

    sleep 60
done
