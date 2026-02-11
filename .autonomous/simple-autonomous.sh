#!/bin/bash
#
# Autonomous Improvement Cycle - Simple Working Version
# Analyzes 63 active tasks, executes improvements
#

set -e

BB5_DIR="/opt/blackbox5"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$TIMESTAMP] 🚀 Autonomous Improvement Cycle"
echo "[$TIMESTAMP] Scanning system for improvements..."

# Count tasks
ACTIVE_COUNT=$(find "$BB5_DIR/5-project-memory/blackbox5/tasks/active" -maxdepth 1 -type d | grep "TASK-" | wc -l)
echo "[$TIMESTAMP] 📊 Found $ACTIVE_COUNT active tasks"

# Simple autonomous analysis
IMPROVEMENTS_FOUND=0
TASKS_CREATED=0
TASKS_EXECUTED=0

# Check for stuck tasks
for taskfile in $(find "$BB5_DIR/5-project-memory/blackbox5/tasks/active" -name "task.md"); do
    TASK_DIR=$(dirname "$taskfile")
    TASK_ID=$(basename "$TASK_DIR")
    
    if grep -q "**Status:** in_progress" "$taskfile"; then
        FILE_AGE=$(($(date +%s) - $(stat -c %Y "$taskfile")))
        
        if [ $FILE_AGE -gt 14400 ]; then
            echo "[$TIMESTAMP] ⚠️ Stuck task: $TASK_ID"
            
            IMPROVEMENT_ID="TASK-AUTO-$(date +%s)"
            IMPROVEMENT_DIR="$BB5_DIR/5-project-memory/blackbox5/tasks/active/$IMPROVEMENT_ID"
            mkdir -p "$IMPROVEMENT_DIR"
            
            echo "# $IMPROVEMENT_ID: Unclaim Stuck Task" > "$IMPROVEMENT_DIR/task.md"
            echo "" >> "$IMPROVEMENT_DIR/task.md"
            echo "**Status:** in_progress" >> "$IMPROVEMENT_DIR/task.md"
            echo "**Priority:** HIGH" >> "$IMPROVEMENT_DIR/task.md"
            echo "**Type:** autonomous_improvement" >> "$IMPROVEMENT_DIR/task.md"
            echo "**Category:** stuck_tasks" >> "$IMPROVEMENT_DIR/task.md"
            echo "**Created:** $TIMESTAMP" >> "$IMPROVEMENT_DIR/task.md"
            echo "**Agent:** autonomous" >> "$IMPROVEMENT_DIR/task.md"
            echo "**ROI Score:** 50" >> "$IMPROVEMENT_DIR/task.md"
            echo "" >> "$IMPROVEMENT_DIR/task.md"
            echo "## Problem" >> "$IMPROVEMENT_DIR/task.md"
            echo "Task $TASK_ID has been in 'in_progress' status for >4 hours." >> "$IMPROVEMENT_DIR/task.md"
            echo "" >> "$IMPROVEMENT_DIR/task.md"
            echo "## Current State" >> "$IMPROVEMENT_DIR/task.md"
            echo "Task file: $taskfile" >> "$IMPROVEMENT_DIR/task.md"
            echo "File age: $FILE_AGE seconds" >> "$IMPROVEMENT_DIR/task.md"
            echo "" >> "$IMPROVEMENT_DIR/task.md"
            echo "## Proposed Fix" >> "$IMPROVEMENT_DIR/task.md"
            echo "Unclaim the stuck task and return it to backlog." >> "$IMPROVEMENT_DIR/task.md"
            
            TASKS_CREATED=$((TASKS_CREATED + 1))
            IMPROVEMENTS_FOUND=$((IMPROVEMENTS_FOUND + 1))
            
            sed -i 's/**Status:** in_progress/**Status:** pending/' "$taskfile"
            
            echo "[$TIMESTAMP] 🔧 Executed: Unclaimed $TASK_ID"
            TASKS_EXECUTED=$((TASKS_EXECUTED + 1))
        fi
    done

# Summary
echo "[$TIMESTAMP] 📊 Summary:"
echo "[$TIMESTAMP]   - Tasks analyzed: $ACTIVE_COUNT"
echo "[$TIMESTAMP]   - Improvements found: $IMPROVEMENTS_FOUND"
echo "[$TIMESTAMP]   - Tasks created: $TASKS_CREATED"
echo "[$TIMESTAMP]   - Tasks executed: $TASKS_EXECUTED"

if [ "$IMPROVEMENTS_FOUND" -eq 0 ]; then
    echo "[$TIMESTAMP] ℹ️ No improvements needed at this time"
elif [ "$TASKS_EXECUTED" -eq 0 ]; then
    echo "[$TIMESTAMP] ⚠️ Improvements found but not executed"
else
    echo "[$TIMESTAMP] 🎯 Executed $TASKS_EXECUTED improvements"
fi

echo "[$TIMESTAMP] ✅ Autonomous cycle complete"
exit 0
