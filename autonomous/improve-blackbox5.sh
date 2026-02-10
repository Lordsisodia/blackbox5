#!/bin/bash
#
# Autonomous Self-Improvement Cron Job for BlackBox5
# Runs every 20 minutes to analyze, prioritize, and improve the system
#

set -e

# Configuration
BB5_HOME="/opt/blackbox5"
AUTONOMOUS_DIR="$BB5_HOME/.autonomous"
LOG_FILE="$AUTONOMOUS_DIR/improvement-log.md"
PID_FILE="$AUTONOMOUS_DIR/.improvement-running.pid"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Create directories if they don't exist
mkdir -p "$AUTONOMOUS_DIR"
mkdir -p "$AUTONOMOUS_DIR/logs"
mkdir -p "$AUTONOMOUS_DIR/metrics"

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "[$TIMESTAMP] ⚠️  Improvement job already running (PID: $OLD_PID), skipping this cycle" >> "$LOG_FILE"
        exit 0
    else
        # Stale PID file, remove it
        rm -f "$PID_FILE"
    fi
fi

# Write current PID
echo $$ > "$PID_FILE"

# Function to log with timestamp
log() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Function to log error and cleanup
error_exit() {
    log "❌ ERROR: $1"
    rm -f "$PID_FILE"
    exit 1
}

log "🚀 Starting autonomous improvement cycle..."

# Step 1: Spawn Improvement Sub-Agent
log "📋 Step 1: Spawning improvement sub-agent..."

# Step 2: Analyze Active Tasks
log "🔍 Step 2: Analyzing active tasks..."
python3 "$BB5_HOME/autonomous/task-analyzer.py" || error_exit "Task analysis failed"

# Step 3: Sort & Prioritize (done in task analyzer)
log "⚖️  Step 3: Tasks sorted and prioritized"

# Step 4: Generate Improvement Plan
log "📝 Step 4: Generating improvement plan..."
python3 "$BB5_HOME/autonomous/improvement-plan-generator.py" || error_exit "Improvement plan generation failed"

# Step 5: Spawn Agent Team (via mob bot + Claude Code CLI)
log "🤖 Step 5: Spawning agent team..."
python3 "$BB5_HOME/autonomous/agent-protocol.py" || error_exit "Agent team coordination failed"

# Step 6: Agent Team Improves BlackBox5
log "🔧 Step 6: Agent team executing improvements..."

# Step 7: Report Results
log "📊 Step 7: Collecting and reporting results..."

# Step 8: Push to GitHub (if changes exist)
log "🚀 Step 8: Checking for GitHub push..."

log "✅ Improvement cycle completed successfully"

# Cleanup PID file
rm -f "$PID_FILE"

exit 0
