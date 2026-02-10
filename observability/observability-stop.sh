#!/bin/bash
# BlackBox5 Observability System - Stop Script

set -e

BB5_ROOT="${BB5_ROOT:-/opt/blackbox5}"
OBSERVABILITY_DIR="$BB5_ROOT/observability"
PID_DIR="$OBSERVABILITY_DIR/pids"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Stopping BlackBox5 Observability System...${NC}"

# Function to stop a service
stop_service() {
    local name="$1"
    local pid_file="$PID_DIR/$2"

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping $name (PID: $pid)...${NC}"
            kill "$pid"
            # Wait for process to stop
            local count=0
            while ps -p "$pid" > /dev/null 2>&1 && [ $count -lt 10 ]; do
                sleep 1
                count=$((count + 1))
            done

            if ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${YELLOW}Force stopping $name...${NC}"
                kill -9 "$pid"
            fi

            rm -f "$pid_file"
            echo -e "${GREEN}✓ $name stopped${NC}"
        else
            echo -e "${YELLOW}⚠ $name not running (stale PID file)${NC}"
            rm -f "$pid_file"
        fi
    else
        echo -e "${YELLOW}⚠ $name not running (no PID file)${NC}"
    fi
}

# Stop services
stop_service "Dashboard API" "dashboard-api.pid"
stop_service "Cost Tracker" "cost-tracker.pid"
stop_service "Log Pipeline" "log-pipeline.pid"
stop_service "Health Checks" "health-checks.pid"

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Observability System Stopped${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To start the system again:"
echo "  $0 start"
echo ""
