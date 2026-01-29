#!/bin/bash
# Telemetry and monitoring for Legacy runs
# Tracks performance, errors, and system health

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TELEMETRY_DIR="$PROJECT_DIR/.Autonomous/telemetry"
CURRENT_RUN_DIR=""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Initialize telemetry
init_telemetry() {
    mkdir -p "$TELEMETRY_DIR"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    TELEMETRY_FILE="$TELEMETRY_DIR/run-$TIMESTAMP.json"

    cat > "$TELEMETRY_FILE" << EOF
{
  "run_id": "$TIMESTAMP",
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "starting",
  "events": [],
  "metrics": {
    "files_read": 0,
    "files_written": 0,
    "commands_executed": 0,
    "errors": 0,
    "warnings": 0
  },
  "phases": {
    "initialization": "pending",
    "task_selection": "pending",
    "execution": "pending",
    "documentation": "pending",
    "completion": "pending"
  }
}
EOF
    echo "$TELEMETRY_FILE"
}

# Log an event
log_event() {
    local type="$1"
    local message="$2"
    local file="$3"

    if [ -z "$file" ]; then
        file=$(ls -t "$TELEMETRY_DIR"/run-*.json 2>/dev/null | head -1)
    fi

    if [ -f "$file" ]; then
        local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        local event="{\"time\": \"$timestamp\", \"type\": \"$type\", \"message\": \"$message\"}"

        # Update metrics based on type
        case "$type" in
            "error")
                jq '.metrics.errors += 1' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
                echo -e "${RED}[ERROR]${NC} $message"
                ;;
            "warning")
                jq '.metrics.warnings += 1' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
                echo -e "${YELLOW}[WARN]${NC} $message"
                ;;
            "success")
                echo -e "${GREEN}[OK]${NC} $message"
                ;;
            "info")
                echo -e "${BLUE}[INFO]${NC} $message"
                ;;
            "phase")
                echo -e "${CYAN}[PHASE]${NC} $message"
                ;;
        esac

        # Add event to array
        jq ".events += [$event]" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    fi
}

# Update phase status
update_phase() {
    local phase="$1"
    local status="$2"
    local file=$(ls -t "$TELEMETRY_DIR"/run-*.json 2>/dev/null | head -1)

    if [ -f "$file" ]; then
        jq ".phases.$phase = \"$status\"" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        log_event "phase" "Phase '$phase' is now $status" "$file"
    fi
}

# Increment metric
increment_metric() {
    local metric="$1"
    local file=$(ls -t "$TELEMETRY_DIR"/run-*.json 2>/dev/null | head -1)

    if [ -f "$file" ]; then
        jq ".metrics.$metric += 1" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    fi
}

# Mark run complete
complete_run() {
    local status="$1"
    local file=$(ls -t "$TELEMETRY_DIR"/run-*.json 2>/dev/null | head -1)

    if [ -f "$file" ]; then
        jq ".status = \"$status\" | .end_time = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        log_event "info" "Run completed with status: $status" "$file"
    fi
}

# Display current status
show_status() {
    local file=$(ls -t "$TELEMETRY_DIR"/run-*.json 2>/dev/null | head -1)

    if [ -f "$file" ]; then
        echo ""
        echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
        echo -e "${CYAN}  Legacy Telemetry${NC}"
        echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
        echo ""

        # Show phases
        echo -e "${BLUE}Phases:${NC}"
        jq -r '.phases | to_entries[] | "  \(.key): \(.value)"' "$file" | while read line; do
            if echo "$line" | grep -q "complete"; then
                echo -e "  ${GREEN}✓${NC} $line"
            elif echo "$line" | grep -q "in_progress"; then
                echo -e "  ${YELLOW}▶${NC} $line"
            elif echo "$line" | grep -q "failed"; then
                echo -e "  ${RED}✗${NC} $line"
            else
                echo -e "  ${BLUE}○${NC} $line"
            fi
        done

        echo ""
        echo -e "${BLUE}Metrics:${NC}"
        jq -r '.metrics | to_entries[] | "  \(.key): \(.value)"' "$file"

        echo ""
        echo -e "${BLUE}Recent Events:${NC}"
        jq -r '.events[-5:] | .[] | "  [\(.type)] \(.message)"' "$file" 2>/dev/null || echo "  No events yet"

        echo ""
    fi
}

# Watch mode - continuous monitoring
watch_mode() {
    while true; do
        clear
        show_status
        sleep 5
    done
}

# Command dispatch
case "$1" in
    init)
        init_telemetry
        ;;
    event)
        log_event "$2" "$3"
        ;;
    phase)
        update_phase "$2" "$3"
        ;;
    metric)
        increment_metric "$2"
        ;;
    complete)
        complete_run "$2"
        ;;
    status)
        show_status
        ;;
    watch)
        watch_mode
        ;;
    *)
        echo "Usage: $0 {init|event|phase|metric|complete|status|watch}"
        echo ""
        echo "Commands:"
        echo "  init              - Initialize telemetry for new run"
        echo "  event <type> <msg> - Log an event (error|warning|success|info)"
        echo "  phase <name> <status> - Update phase status"
        echo "  metric <name>     - Increment a metric"
        echo "  complete <status> - Mark run complete"
        echo "  status            - Show current status"
        echo "  watch             - Continuous monitoring"
        ;;
esac
