#!/bin/bash
#
# Autonomous Task Runner - Uses BlackBox5 Orchestrator
# Every 30 minutes: Scans, identifies improvements, executes via bb5-orchestrator
#

set -e

BB5_DIR="/opt/blackbox5"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$TIMESTAMP] 🚀 Autonomous Task Runner"
echo "[$TIMESTAMP] Using BlackBox5 Orchestrator for coordination"

# Ensure bb5-orchestrator is in PATH
if ! command -v bb5-orchestrator &>/dev/null; then
    echo "[$TIMESTAMP] ⚠️  bb5-orchestrator not found in PATH"
    echo "[$TIMESTAMP] 📍 Adding to PATH: $BB5_DIR/bin"
    export PATH="$BB5_DIR/bin:$PATH"
fi

# Route to BlackBox5 Orchestrator
echo "[$TIMESTAMP] 🎯 Routing to bb5-orchestrator..."

cd "$BB5_DIR"
export PATH="$BB5_DIR/bin:$PATH"

# Call bb5-orchestrator route with the task
bb5-orchestrator route 2>&1 | head -50

echo "[$TIMESTAMP] ✅ Autonomous cycle complete"
exit 0
