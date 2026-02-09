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

# Telegram configuration
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-7643203581}"
TELEGRAM_TOPIC_ID="${TELEGRAM_TOPIC_ID:-}"  # Set this for topic-specific updates

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

# Send Telegram notification
send_telegram_update() {
    local run_id="$1"
    local status="$2"
    local action="$3"
    local run_folder="$4"
    local duration="${5:-unknown}"

    # Determine emoji based on status
    local emoji="📊"
    case "$status" in
        COMPLETED) emoji="✅" ;;
        FAILED) emoji="❌" ;;
        PARTIAL) emoji="⚠️" ;;
    esac

    # Build message
    local message="${emoji} <b>BB5 Run Complete</b>%0A"
    message+="<code>${run_id}</code>%0A"
    message+="━━━━━━━━━━━━━━━━━━━━━━━%0A%0A"

    # Status and action
    message+="<b>Status:</b> ${status}%0A"
    message+="<b>Action:</b> ${action}%0A"
    message+="<b>Duration:</b> ${duration}s%0A%0A"

    # Read git stats if available
    if [ -f "$run_folder/git.log" ]; then
        local commits=$(grep -c "commit" "$run_folder/git.log" 2>/dev/null || echo "0")
        local pushed=$(grep -c "push" "$run_folder/git.log" 2>/dev/null || echo "0")
        if [ "$commits" -gt 0 ] || [ "$pushed" -gt 0 ]; then
            message+="<b>🔄 Git</b>%0A"
            [ "$commits" -gt 0 ] && message+="• Commits: ${commits}%0A"
            [ "$pushed" -gt 0 ] && message+="• Pushed: yes%0A"
            message+="%0A"
        fi
    fi

    # Read results if available
    if [ -f "$run_folder/RESULTS.md" ]; then
        local result_summary=$(grep -A 5 "## Outcomes" "$run_folder/RESULTS.md" 2>/dev/null | tail -n +2 | head -3 | tr '\n' ' ' | sed 's/  */ /g' | cut -c1-100)
        if [ -n "$result_summary" ]; then
            message+="<b>📋 Result:</b>%0A${result_summary}...%0A%0A"
        fi
    fi

    # Add next action hint
    case "$status" in
        COMPLETED)
            message+"<i>✓ Run completed successfully. Starting next cycle...</i>"
            ;;
        FAILED)
            message+"<i>⚠ Run failed. Will retry (failure ${CONSECUTIVE_FAILURES}/${MAX_CONSECUTIVE_FAILURES})</i>"
            ;;
        PARTIAL)
            message+"<i>⏳ Run partial. Continuing in next cycle...</i>"
            ;;
    esac

    # Send to Telegram
    local payload="chat_id=${TELEGRAM_CHAT_ID}&text=${message}&parse_mode=HTML"
    if [ -n "$TELEGRAM_TOPIC_ID" ]; then
        payload="${payload}&message_thread_id=${TELEGRAM_TOPIC_ID}"
    fi

    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "$payload" > /dev/null 2>&1 || true
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

# Send startup notification to Telegram
startup_message="🤖%20<b>MoltBot%20RALF%20Manager</b>%20started%0A"
startup_message+="━━━━━━━━━━━━━━━━━━━━━━━%0A"
startup_message+="<i>Will%20report%20after%20each%20run%20completes</i>"
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=${TELEGRAM_CHAT_ID}&text=${startup_message}&parse_mode=HTML" \
    > /dev/null 2>&1 || true

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

    # Record start time
    CYCLE_START_TIME=$(date +%s)

    # Run RALF single cycle
    set +e
    "$RALF_SCRIPT" 2>&1 | tee -a "$LOG_FILE"
    RALF_EXIT_CODE=$?
    set -e

    # Calculate duration
    CYCLE_END_TIME=$(date +%s)
    CYCLE_DURATION=$((CYCLE_END_TIME - CYCLE_START_TIME))

    # Get latest run
    LATEST_RUN=$(ls -1t "$RUNS_DIR" 2>/dev/null | head -1)
    LATEST_STATUS="UNKNOWN"
    LATEST_ACTION="unknown"
    if [ -n "$LATEST_RUN" ] && [ -f "$RUNS_DIR/$LATEST_RUN/status.txt" ]; then
        LATEST_STATUS=$(cat "$RUNS_DIR/$LATEST_RUN/status.txt")
    fi
    if [ -n "$LATEST_RUN" ] && [ -f "$RUNS_DIR/$LATEST_RUN/context.yaml" ]; then
        LATEST_ACTION=$(grep "action:" "$RUNS_DIR/$LATEST_RUN/context.yaml" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "unknown")
    fi

    log ""
    log "RALF Cycle Complete"
    log "  Exit Code: $RALF_EXIT_CODE"
    log "  Latest Run: ${LATEST_RUN:-none}"
    log "  Status: $LATEST_STATUS"

    # Send Telegram update
    if [ -n "$LATEST_RUN" ]; then
        send_telegram_update "$LATEST_RUN" "$LATEST_STATUS" "$LATEST_ACTION" "$RUNS_DIR/$LATEST_RUN" "$CYCLE_DURATION"
    fi

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
