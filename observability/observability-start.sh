#!/bin/bash
# BlackBox5 Observability System - Start Script

set -e

BB5_ROOT="${BB5_ROOT:-/opt/blackbox5}"
OBSERVABILITY_DIR="$BB5_ROOT/observability"
PID_DIR="$OBSERVABILITY_DIR/pids"
LOG_DIR="$OBSERVABILITY_DIR/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting BlackBox5 Observability System...${NC}"

# Create directories
mkdir -p "$PID_DIR"
mkdir -p "$LOG_DIR"

# Check Python dependencies
echo -e "${YELLOW}Checking Python dependencies...${NC}"
python3 -c "import fastapi, uvicorn" 2>/dev/null || {
    echo -e "${RED}Error: FastAPI and Uvicorn required. Install with: pip install fastapi uvicorn${NC}"
    exit 1
}

# Function to check if a service is already running
is_running() {
    local pid_file="$1"
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            rm -f "$pid_file"
        fi
    fi
    return 1
}

# Start Dashboard API
if ! is_running "$PID_DIR/dashboard-api.pid"; then
    echo -e "${YELLOW}Starting Dashboard API...${NC}"
    cd "$OBSERVABILITY_DIR/dashboard"
    nohup python3 dashboard_api.py > "$LOG_DIR/dashboard-api.log" 2>&1 &
    echo $! > "$PID_DIR/dashboard-api.pid"
    echo -e "${GREEN}✓ Dashboard API started (PID: $!)${NC}"
    echo -e "  URL: http://77.42.66.40:8080"
    echo -e "  Docs: http://77.42.66.40:8080/docs"
else
    echo -e "${YELLOW}⚠ Dashboard API already running${NC}"
fi

# Start Cost Tracker (as a background daemon)
if ! is_running "$PID_DIR/cost-tracker.pid"; then
    echo -e "${YELLOW}Starting Cost Tracker daemon...${NC}"
    cd "$OBSERVABILITY_DIR/cost_tracker"
    nohup python3 -c "
import sys
sys.path.insert(0, '$BB5_ROOT/bin/lib')
from cost_tracker import CostTracker
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

tracker = CostTracker()
print('Cost Tracker daemon started')

# Keep alive
while True:
    time.sleep(3600)  # Check every hour
" > "$LOG_DIR/cost-tracker.log" 2>&1 &
    echo $! > "$PID_DIR/cost-tracker.pid"
    echo -e "${GREEN}✓ Cost Tracker started (PID: $!)${NC}"
else
    echo -e "${YELLOW}⚠ Cost Tracker already running${NC}"
fi

# Start Log Pipeline (as a background daemon)
if ! is_running "$PID_DIR/log-pipeline.pid"; then
    echo -e "${YELLOW}Starting Log Pipeline daemon...${NC}"
    cd "$OBSERVABILITY_DIR/log_pipeline"
    nohup python3 -c "
import sys
sys.path.insert(0, '$BB5_ROOT/bin/lib')
from log_pipeline import LogPipeline
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

pipeline = LogPipeline()
print('Log Pipeline daemon started')

# Ingest from Redis streams periodically
while True:
    try:
        # Read from stream:messages
        count = pipeline.ingest_from_redis_stream('stream:messages', batch_size=100)
        if count > 0:
            print(f'Ingested {count} log entries from stream:messages')
    except Exception as e:
        print(f'Error ingesting logs: {e}')
    time.sleep(30)  # Check every 30 seconds
" > "$LOG_DIR/log-pipeline.log" 2>&1 &
    echo $! > "$PID_DIR/log-pipeline.pid"
    echo -e "${GREEN}✓ Log Pipeline started (PID: $!)${NC}"
else
    echo -e "${YELLOW}⚠ Log Pipeline already running${NC}"
fi

# Start Health Checks (if not already started by bb5-health daemon)
if ! is_running "$PID_DIR/health-checks.pid"; then
    echo -e "${YELLOW}Starting Health Checks daemon...${NC}"
    cd "$OBSERVABILITY_DIR/health_checks"
    nohup python3 -c "
import sys
sys.path.insert(0, '$BB5_ROOT/bin/lib')
from health_checks import HealthChecker
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

checker = HealthChecker()
print('Health Checks daemon started')

# Run health checks periodically
while True:
    try:
        results = checker.check_all()
        timestamp = datetime.now().isoformat()
        status_summary = ', '.join([f'{k}={v.status.value}' for k, v in results.items()])
        print(f'[{timestamp}] Health check: {status_summary}')
    except Exception as e:
        print(f'Error running health checks: {e}')
    time.sleep(60)  # Check every minute
" > "$LOG_DIR/health-checks.log" 2>&1 &
    echo $! > "$PID_DIR/health-checks.pid"
    echo -e "${GREEN}✓ Health Checks started (PID: $!)${NC}"
else
    echo -e "${YELLOW}⚠ Health Checks already running${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Observability System Started${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Dashboard:    http://77.42.66.40:8080"
echo "API Docs:     http://77.42.66.40:8080/docs"
echo "Health Check: http://77.42.66.40:8080/health"
echo ""
echo "Logs: $LOG_DIR"
echo "PIDs: $PID_DIR"
echo ""
echo "To stop the system:"
echo "  $0 stop"
echo ""
