#!/bin/bash
# Ralph Autonomous Agent - Startup Script
# Usage: ./start-ralph.sh [mode]
# Modes: setup, feature, idea, test, full

set -e

# Configuration
RALPH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$RALPH_DIR/CONFIG.yaml"
LOG_DIR="$RALPH_DIR/LOGS"
STATE_DIR="$RALPH_DIR/STATE"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_LOG="$LOG_DIR/sessions/session-$TIMESTAMP.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$SESSION_LOG"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$SESSION_LOG"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$SESSION_LOG"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$SESSION_LOG"
}

# Check if running on allowed branch
check_branch() {
    log "Checking git branch..."

    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

    if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
        log_error "CRITICAL: Currently on '$CURRENT_BRANCH' branch!"
        log_error "Ralph is forbidden from running on main/master."
        log_error "Please switch to dev branch: git checkout dev"
        exit 1
    fi

    log_success "On branch: $CURRENT_BRANCH (allowed)"
    echo "branch: $CURRENT_BRANCH" >> "$STATE_DIR/current-session.yaml"
}

# Check API availability
check_apis() {
    log "Checking API availability..."

    # Check GLM
    if command -v claude &> /dev/null; then
        log_success "GLM API available (claude command)"
        GLM_STATUS="available"
    else
        log_warning "GLM API not available (claude command not found)"
        GLM_STATUS="unavailable"
    fi

    # Check Kimi
    if command -v cso-kimi &> /dev/null; then
        log_success "Kimi API available (cso-kimi command)"
        KIMI_STATUS="available"
    else
        log_warning "Kimi API not available (cso-kimi command not found)"
        KIMI_STATUS="unavailable"
    fi

    if [[ "$GLM_STATUS" == "unavailable" && "$KIMI_STATUS" == "unavailable" ]]; then
        log_error "No APIs available! Cannot start Ralph."
        exit 1
    fi

    echo "api_glm: $GLM_STATUS" >> "$STATE_DIR/current-session.yaml"
    echo "api_kimi: $KIMI_STATUS" >> "$STATE_DIR/current-session.yaml"
}

# Initialize session state
init_session() {
    log "Initializing session..."

    mkdir -p "$LOG_DIR/sessions" "$LOG_DIR/errors" "$LOG_DIR/performance" "$STATE_DIR"

    cat > "$STATE_DIR/current-session.yaml" << EOF
session:
  id: "ralph-$TIMESTAMP"
  start_time: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  status: "starting"
  mode: "$MODE"
  host: "$(hostname)"
  pid: $$
EOF

    log_success "Session initialized: ralph-$TIMESTAMP"
}

# Run setup agent
run_setup() {
    log "Running setup agent..."

    # Check project structure
    log "  Checking BlackBox 5 memory structure..."
    BB5_MEM="$RALPH_DIR/../5-project-memory/siso-internal"

    if [[ -d "$BB5_MEM" ]]; then
        log_success "  BlackBox 5 memory found"

        # Check key files
        for file in "STATE.yaml" "ACTIVE.md" "WORK-LOG.md"; do
            if [[ -f "$BB5_MEM/$file" ]]; then
                log_success "  Found: $file"
            else
                log_warning "  Missing: $file"
            fi
        done
    else
        log_error "  BlackBox 5 memory not found at $BB5_MEM"
    fi

    # Check projects
    log "  Checking configured projects..."
    # This would parse CONFIG.yaml in a real implementation

    log_success "Setup agent complete"
}

# Main execution
main() {
    MODE="${1:-full}"

    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              Ralph Autonomous Agent v1.0                   ║"
    echo "║                                                            ║"
    echo "║  Mode: $MODE"
    echo "║  Time: $(date)"
    echo "║  Log:  $SESSION_LOG"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    # Initialize
    init_session

    # Safety checks
    check_branch
    check_apis

    # Run based on mode
    case "$MODE" in
        setup)
            run_setup
            ;;
        feature)
            log "Feature development mode - would run feature agent"
            ;;
        idea)
            log "Idea generation mode - would run idea agent"
            ;;
        test)
            log "Testing mode - would run test agent"
            ;;
        full)
            run_setup
            log "Full mode - would start autonomous loop"
            log "This is where the main Ralph loop would run"
            ;;
        *)
            log_error "Unknown mode: $MODE"
            echo "Usage: $0 [setup|feature|idea|test|full]"
            exit 1
            ;;
    esac

    # Update session state
    cat > "$STATE_DIR/current-session.yaml" << EOF
session:
  id: "ralph-$TIMESTAMP"
  start_time: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  end_time: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  status: "completed"
  mode: "$MODE"
  host: "$(hostname)"
EOF

    echo ""
    log_success "Ralph session completed"
    echo ""
}

# Handle interrupts
trap 'log_warning "Interrupted by user"; exit 130' INT TERM

# Run main
main "$@"
