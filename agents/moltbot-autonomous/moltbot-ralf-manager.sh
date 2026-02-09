#!/bin/bash
# Moltbot RALF Manager
# Manages RALF single-cycle execution with immediate restart
# This is the controller that Moltbot uses to orchestrate BB5 improvement

set -e

BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
RALF_SCRIPT="$BB5_DIR/bin/ralf-loops/loops/ralf-core-single-cycle.sh"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"
LOG_FILE="$BB5_DIR/.autonomous/logs/moltbot-ralf-manager.log"
MAX_CONSECUTIVE_FAILURES=3
CONSECUTIVE_FAILURES=0

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} [MOLTBOT-RALF] $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} [MOLTBOT-RALF] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')]${NC} [MOLTBOT-RALF] $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')]${NC} [MOLTBOT-RALF] $1" | tee -a "$LOG_FILE"
}

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

log "═══════════════════════════════════════════════════"
log "Moltbot RALF Manager Starting"
log "═══════════════════════════════════════════════════"
log "RALF Script: $RALF_SCRIPT"
log "Runs Directory: $RUNS_DIR"
log "Log File: $LOG_FILE"
log ""

# Check if RALF script exists
if [ ! -f "$RALF_SCRIPT" ]; then
    log_error "RALF script not found: $RALF_SCRIPT"
    exit 1
fi

# Main management loop
while true; do
    log ""
    log "───────────────────────────────────────────────────"
    log "Starting RALF Single Cycle..."
    log "───────────────────────────────────────────────────"

    # Run RALF single cycle
    set +e
    "$RALF_SCRIPT" 2>&1 | tee -a "$LOG_FILE"
    RALF_EXIT_CODE=$?
    set -e

    # Get latest run
    LATEST_RUN=$(ls -1t "$RUNS_DIR" 2>/dev/null | head -1)
    LATEST_STATUS="UNKNOWN"
    if [ -n "$LATEST_RUN" ] && [ -f "$RUNS_DIR/$LATEST_RUN/status.txt" ]; then
        LATEST_STATUS=$(cat "$RUNS_DIR/$LATEST_RUN/status.txt")
    fi

    log ""
    log "RALF Cycle Complete"
    log "  Exit Code: $RALF_EXIT_CODE"
    log "  Latest Run: ${LATEST_RUN:-none}"
    log "  Status: $LATEST_STATUS"

    # Handle exit code
    case $RALF_EXIT_CODE in
        0)
            # COMPLETED - success
            log_success "Cycle completed successfully"
            CONSECUTIVE_FAILURES=0
            ;;
        1)
            # FAILED - error
            log_error "Cycle failed"
            CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
            ;;
        2)
            # PARTIAL - needs continuation
            log_warn "Cycle partial - will continue"
            CONSECUTIVE_FAILURES=0
            ;;
        *)
            # Unknown exit code
            log_warn "Unknown exit code: $RALF_EXIT_CODE"
            CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
            ;;
    esac

    # Check for too many failures
    if [ $CONSECUTIVE_FAILURES -ge $MAX_CONSECUTIVE_FAILURES ]; then
        log_error "Too many consecutive failures ($CONSECUTIVE_FAILURES)"
        log_error "Stopping Moltbot RALF Manager"
        exit 1
    fi

    # Pause before restart - longer if no AI provider (to avoid spinning)
    if command -v glm &> /dev/null; then
        log "GLM-4.7 detected - Restarting in 5 seconds..."
        sleep 5
    elif [ -n "$ANTHROPIC_API_KEY" ] || [ -f "$HOME/.config/claude/config.json" ]; then
        log "Claude detected - Restarting in 5 seconds..."
        sleep 5
    else
        log_warn "No AI provider (GLM or Claude) - waiting 60 seconds"
        log_warn "Install GLM: curl -fsSL https://glm.ai/install.sh | sh"
        log_warn "Or set ANTHROPIC_API_KEY for Claude"
        sleep 60
    fi

done
