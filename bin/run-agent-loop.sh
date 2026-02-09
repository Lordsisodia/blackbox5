#!/bin/bash
# run-agent-loop.sh - Continuously run agent runner
# This keeps the agent queue processing

set -e

BB5_DIR="$HOME/.blackbox5/5-project-memory/blackbox5"
LOG_FILE="$BB5_DIR/.autonomous/logs/agent-loop.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date -Iseconds)] Agent loop starting..." | tee -a "$LOG_FILE"

# Run every 10 seconds
while true; do
    python3 "$HOME/.blackbox5/bin/agent-runner.py" 2>&1 | tee -a "$LOG_FILE" | tail -5
    sleep 10
done
