#!/bin/bash
# RALF Status Reporter - Shows current state for MoltBot integration

BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"
LOG_FILE="$BB5_DIR/.autonomous/logs/ralf-core.log"

echo "=== RALF Autonomous Loop Status ==="
echo "Timestamp: $(date)"
echo ""

# Check if ralf-core is running
if pgrep -f "ralf-core.sh" > /dev/null; then
    echo "RALF-Core: RUNNING"
    PID=$(pgrep -f "ralf-core.sh" | head -1)
    echo "   PID: $PID"
    echo "   Uptime: $(ps -o etime= -p $PID 2>/dev/null || echo 'unknown')"
else
    echo "RALF-Core: NOT RUNNING"
fi

# Check if Claude is running
if pgrep -x "claude" > /dev/null; then
    echo "Claude Code: RUNNING"
    CLAUDE_PID=$(pgrep -x "claude" | head -1)
    echo "   PID: $CLAUDE_PID"
    echo "   Running: $(ps -o etime= -p $CLAUDE_PID 2>/dev/null || echo 'unknown')"
else
    echo "Claude Code: NOT RUNNING"
fi

echo ""
echo "=== Current Task ==="
# Find the most recent run folder
LATEST_RUN=$(ls -td "$RUNS_DIR"/run-* 2>/dev/null | head -1)
if [ -n "$LATEST_RUN" ]; then
    TASK_NAME=$(basename "$LATEST_RUN" | sed 's/run-[0-9]*_[0-9]*-//')
    echo "Task: $TASK_NAME"
    echo "Run Folder: $LATEST_RUN"

    # Check status
    if [ -f "$LATEST_RUN/status.txt" ]; then
        STATUS=$(cat "$LATEST_RUN/status.txt")
        echo "Status: $STATUS"
    else
        echo "Status: IN_PROGRESS (no status file yet)"
    fi

    # Show output preview
    if [ -f "$LATEST_RUN/claude_output.log" ]; then
        OUTPUT_SIZE=$(wc -c < "$LATEST_RUN/claude_output.log")
        echo "Output Size: $OUTPUT_SIZE bytes"
        if [ "$OUTPUT_SIZE" -gt 0 ]; then
            echo ""
            echo "=== Latest Output (last 20 lines) ==="
            tail -20 "$LATEST_RUN/claude_output.log"
        fi
    fi
else
    echo "No active runs found"
fi

echo ""
echo "=== Recent Log Entries (last 10) ==="
tail -10 "$LOG_FILE" 2>/dev/null || echo "No log file found"

echo ""
echo "=== Task Queue ==="
TASK_COUNT=$(find "$BB5_DIR/5-project-memory/blackbox5/.autonomous/tasks/active" -name "TASK-*.md" 2>/dev/null | wc -l)
echo "Active Tasks: $TASK_COUNT"
find "$BB5_DIR/5-project-memory/blackbox5/.autonomous/tasks/active" -name "TASK-*.md" -exec grep -l "Status: pending\|Status: partial" {} \; 2>/dev/null | wc -l | xargs echo "Pending/Partial:"
