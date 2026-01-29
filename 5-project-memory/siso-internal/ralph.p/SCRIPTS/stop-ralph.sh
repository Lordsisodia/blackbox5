#!/bin/bash
# Ralph Autonomous Agent - Stop Script
# Usage: ./stop-ralph.sh

set -e

RALPH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$RALPH_DIR/STATE"
PID_FILE="$STATE_DIR/ralph.pid"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Stopping Ralph Autonomous Agent...${NC}"

# Check if PID file exists
if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}Found Ralph process (PID: $PID)${NC}"
        echo -e "${BLUE}Sending graceful shutdown signal...${NC}"

        kill -TERM "$PID" 2>/dev/null || true

        # Wait for process to exit
        for i in {1..10}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                echo -e "${GREEN}Ralph stopped gracefully${NC}"
                rm -f "$PID_FILE"
                exit 0
            fi
            sleep 1
        done

        # Force kill if still running
        echo -e "${YELLOW}Force killing Ralph...${NC}"
        kill -KILL "$PID" 2>/dev/null || true
        rm -f "$PID_FILE"
        echo -e "${GREEN}Ralph stopped${NC}"
    else
        echo -e "${YELLOW}Ralph process not running (stale PID file)${NC}"
        rm -f "$PID_FILE"
    fi
else
    echo -e "${YELLOW}No PID file found - Ralph may not be running${NC}"

    # Try to find Ralph processes
    RALPH_PIDS=$(pgrep -f "ralph" || true)
    if [[ -n "$RALPH_PIDS" ]]; then
        echo -e "${YELLOW}Found potential Ralph processes:${NC}"
        echo "$RALPH_PIDS"
        echo -e "${YELLOW}Use 'kill -9 <PID>' to stop manually${NC}"
    fi
fi

# Update session state if exists
CURRENT_SESSION="$STATE_DIR/current-session.yaml"
if [[ -f "$CURRENT_SESSION" ]]; then
    echo -e "${BLUE}Updating session state...${NC}"
    # Add end time to session file
    echo "  stopped_at: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" >> "$CURRENT_SESSION"
    echo "  stop_reason: manual" >> "$CURRENT_SESSION"
fi

echo -e "${GREEN}Ralph shutdown complete${NC}"
