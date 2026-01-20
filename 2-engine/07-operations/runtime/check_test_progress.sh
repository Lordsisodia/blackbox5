#!/bin/bash
# Monitor the autonomous BLACKBOX5 tester progress

LOG_FILE="/tmp/bb5-1000-iter.log"
PID_FILE="/tmp/bb5-tester.pid"

# Check if process is running
if ps -p 97864 > /dev/null 2>&1; then
    echo "✓ Autonomous tester is running (PID: 97864)"
    echo ""

    # Show latest progress
    echo "=== LATEST PROGRESS UPDATE ==="
    grep "PROGRESS UPDATE" "$LOG_FILE" | tail -1
    echo ""

    # Show current iteration
    echo "=== CURRENT STATUS ==="
    grep "Iteration.*complete:" "$LOG_FILE" | tail -1
    echo ""

    # Show server status
    echo "=== SERVER STATUS ==="
    ps aux | grep "interface.api.main" | grep -v grep | head -1
    echo ""

    # Show time elapsed
    START_TIME=$(ps -p 97864 -o lstart=)
    echo "Started at: $START_TIME"
    echo ""

    # Show recent activity
    echo "=== RECENT ACTIVITY (last 20 lines) ==="
    tail -20 "$LOG_FILE"
else
    echo "✗ Autonomous tester is NOT running"
    echo ""
    echo "=== FINAL SUMMARY ==="
    grep "Testing completed" "$LOG_FILE" || echo "Test did not complete cleanly"
    echo ""
    echo "=== TOTAL ITERATIONS ==="
    grep "Iteration.*complete:" "$LOG_FILE" | wc -l | xargs echo "Iterations completed:"
    echo ""
    echo "=== ISSUES FIXED ==="
    grep "Issues fixed:" "$LOG_FILE" | tail -1
fi
