#!/bin/bash
# RALF Autonomous Loop
# Runs from engine, operates on project memory

set -e

# Determine engine path (where this script lives)
ENGINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Project path can be passed as argument
PROJECT_DIR="${1:-$(pwd)}"
PROJECT_AUTONOMOUS="$PROJECT_DIR/.autonomous"

# Detect blackbox5 root from engine location
BLACKBOX5_DIR="$(cd "$ENGINE_DIR/../.." && pwd)"

# Validate project has .autonomous
if [ ! -d "$PROJECT_AUTONOMOUS" ]; then
    echo "Error: No .autonomous folder found at $PROJECT_AUTONOMOUS"
    echo "Usage: $0 [path-to-project]"
    echo "Or run from a directory containing .autonomous/"
    exit 1
fi

# Change to blackbox5 root so Claude has access to everything
cd "$BLACKBOX5_DIR"

# Load routes if available
ROUTES_FILE="$PROJECT_AUTONOMOUS/routes.yaml"
if [ -f "$ROUTES_FILE" ]; then
    echo "[RALF] Loaded routes from $ROUTES_FILE"
    echo "[RALF] Working directory: $BLACKBOX5_DIR (full blackbox5 access)"
fi

# Core paths
PROMPT_FILE="$ENGINE_DIR/prompts/ralf.md"
LOG_DIR="$PROJECT_AUTONOMOUS/LOGS"
TELEMETRY_SCRIPT="$ENGINE_DIR/shell/telemetry.sh"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_LOG="$LOG_DIR/ralf-session-$TIMESTAMP.log"
TELEMETRY_FILE=""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1" | tee -a "$SESSION_LOG"
    if [ -n "$TELEMETRY_FILE" ]; then
        "$TELEMETRY_SCRIPT" event info "$1" "$TELEMETRY_FILE" 2>/dev/null || true
    fi
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$SESSION_LOG"
    if [ -n "$TELEMETRY_FILE" ]; then
        "$TELEMETRY_SCRIPT" event error "$1" "$TELEMETRY_FILE" 2>/dev/null || true
    fi
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$SESSION_LOG"
    if [ -n "$TELEMETRY_FILE" ]; then
        "$TELEMETRY_SCRIPT" event success "$1" "$TELEMETRY_FILE" 2>/dev/null || true
    fi
}

log_phase() {
    echo -e "${CYAN}[PHASE]${NC} $1" | tee -a "$SESSION_LOG"
    if [ -n "$TELEMETRY_FILE" ]; then
        "$TELEMETRY_SCRIPT" phase "$1" "in_progress" "$TELEMETRY_FILE" 2>/dev/null || true
    fi
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$SESSION_LOG"
    if [ -n "$TELEMETRY_FILE" ]; then
        "$TELEMETRY_SCRIPT" event warning "$1" "$TELEMETRY_FILE" 2>/dev/null || true
    fi
}

# Initialize telemetry for this run
init_run() {
    if [ -x "$TELEMETRY_SCRIPT" ]; then
        TELEMETRY_FILE=$("$TELEMETRY_SCRIPT" init "$PROJECT_AUTONOMOUS")
        log "Telemetry initialized: $(basename "$TELEMETRY_FILE")"
    fi
}

# Check we're on safe branch (not main/master)
check_branch() {
    cd "$PROJECT_DIR"
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

    if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
        log_error "CRITICAL: On '$CURRENT_BRANCH' branch! RALF cannot run here."
        exit 1
    fi

    log "Running on branch: $CURRENT_BRANCH"
}

# Check prerequisites
check_prerequisites() {
    log_phase "prerequisites"

    # Check claude is available
    if ! command -v claude &> /dev/null; then
        log_error "claude command not found in PATH"
        exit 1
    fi
    log "✓ claude found"

    # Check prompt file exists
    if [ ! -f "$PROMPT_FILE" ]; then
        log_error "RALF prompt not found at $PROMPT_FILE"
        exit 1
    fi
    log "✓ RALF prompt found"

    # Check active tasks exist
    local active_tasks=$(find "$PROJECT_AUTONOMOUS/tasks/active" -name "*.md" -type f ! -name "index.md" ! -name "TEMPLATE.md" 2>/dev/null | wc -l)
    if [ "$active_tasks" -eq 0 ]; then
        log_warning "No active tasks found"
    else
        log "✓ $active_tasks active task(s) found"
    fi

    # Check jq is available for telemetry
    if ! command -v jq &> /dev/null; then
        log_warning "jq not found - telemetry will be limited"
    fi

    if [ -n "$TELEMETRY_FILE" ]; then
        "$TELEMETRY_SCRIPT" phase prerequisites "complete" "$TELEMETRY_FILE" 2>/dev/null || true
    fi
}

# Display run summary
show_summary() {
    echo ""
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}  Run Summary${NC}"
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════${NC}"
    echo ""
    log "Project: $PROJECT_DIR"
    log "Engine: $ENGINE_DIR"
    log "Session log: $SESSION_LOG"
    if [ -n "$TELEMETRY_FILE" ]; then
        log "Telemetry: $TELEMETRY_FILE"
        "$TELEMETRY_SCRIPT" status 2>/dev/null || true
    fi
    echo ""
}

# Main loop
main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              RALF Autonomous System                        ║"
    echo "║              First Principles Build System                 ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    mkdir -p "$LOG_DIR"

    # Initialize telemetry
    init_run

    log "Starting RALF loop..."
    log "Project: $PROJECT_DIR"
    log "Engine: $ENGINE_DIR"
    log "Logs: $LOG_DIR"

    check_branch
    check_prerequisites

    show_summary

    LOOP_COUNT=0

    while true; do
        LOOP_COUNT=$((LOOP_COUNT + 1))
        log ""
        log "════════════════════════════════════════════════════════════"
        log "Loop iteration: $LOOP_COUNT"
        log "Time: $(date)"
        log "════════════════════════════════════════════════════════════"

        log_phase "execution"

        # Run RALF with full blackbox5 context
        log "Executing: cat ralf.md | claude -p --dangerously-skip-permissions"
        log "Working directory: $BLACKBOX5_DIR"
        echo ""
        echo -e "${YELLOW}--- RALF Output Start ---${NC}"
        echo ""

        # Export paths for the prompt to use
        export RALF_PROJECT_DIR="$PROJECT_DIR"
        export RALF_ENGINE_DIR="$ENGINE_DIR"
        export RALF_BLACKBOX5_DIR="$BLACKBOX5_DIR"

        if ! cat "$PROMPT_FILE" | claude -p --dangerously-skip-permissions 2>&1 | tee -a "$SESSION_LOG"; then
            EXIT_CODE=${PIPESTATUS[0]}
            echo ""
            echo -e "${YELLOW}--- RALF Output End ---${NC}"
            echo ""
            log_error "RALF execution failed with exit code $EXIT_CODE"

            if [ -n "$TELEMETRY_FILE" ]; then
                "$TELEMETRY_SCRIPT" phase execution "failed" "$TELEMETRY_FILE" 2>/dev/null || true
                "$TELEMETRY_SCRIPT" complete "failed" "$TELEMETRY_FILE" 2>/dev/null || true
            fi

            sleep 30
            continue
        fi

        echo ""
        echo -e "${YELLOW}--- RALF Output End ---${NC}"
        echo ""

        # Capture the result for analysis
        RESULT=$(cat "$SESSION_LOG" | tail -100)

        if [ -n "$TELEMETRY_FILE" ]; then
            "$TELEMETRY_SCRIPT" phase execution "complete" "$TELEMETRY_FILE" 2>/dev/null || true
        fi

        # Check for completion
        if echo "$RESULT" | grep -q "<promise>COMPLETE</promise>"; then
            log_success "All tasks complete!"
            log "RALF is done. Exiting loop."

            if [ -n "$TELEMETRY_FILE" ]; then
                "$TELEMETRY_SCRIPT" complete "success" "$TELEMETRY_FILE" 2>/dev/null || true
            fi

            show_summary
            exit 0
        fi

        # Check for blocked status
        if echo "$RESULT" | grep -q "Status: BLOCKED"; then
            log_error "RALF is blocked. Check logs for details."
            log "Continuing in case blockers resolve..."

            if [ -n "$TELEMETRY_FILE" ]; then
                "$TELEMETRY_SCRIPT" event warning "Run blocked" "$TELEMETRY_FILE" 2>/dev/null || true
            fi
        fi

        # Check for partial completion
        if echo "$RESULT" | grep -q "Status: PARTIAL"; then
            log_warning "Task partially completed"

            if [ -n "$TELEMETRY_FILE" ]; then
                "$TELEMETRY_SCRIPT" event warning "Partial completion" "$TELEMETRY_FILE" 2>/dev/null || true
            fi
        fi

        # Brief pause between loops
        log "Waiting 10 seconds before next iteration..."
        sleep 10
    done
}

# Handle interrupts
trap 'log "Interrupted by user"; show_summary; exit 130' INT TERM

# Run
main "$@"
