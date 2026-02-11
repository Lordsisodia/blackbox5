#!/bin/bash
#
# Autonomous Improvement System - Uses BlackBox5 Tasks
# Every 30 minutes: Analyzes active tasks, executes improvements
#

set -e

BB5_DIR="/opt/blackbox5"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$TIMESTAMP] 🚀 Autonomous Improvement Cycle"
echo "[$TIMESTAMP] Scanning system for improvements..."

# Check if we're working on the multi-bot infrastructure task
CURRENT_TASK_FILE="$BB5_DIR/5-project-memory/blackbox5/tasks/active/TASK-AUTO-202602110834/task.md"

if [ -f "$CURRENT_TASK_FILE" ]; then
    echo "[$TIMESTAMP] 📋 Found active task: TASK-AUTO-202602110834 (Persistent Multi-Bot Infrastructure)"
    echo "[$TIMESTAMP] Please continue working on that task for multi-bot system"
    echo "[$TIMESTAMP] Skipping autonomous cycle to avoid conflicts"
    exit 0
fi

# Count active tasks
ACTIVE_COUNT=$(find "$BB5_DIR/5-project-memory/blackbox5/tasks/active" -maxdepth 1 -type d | grep "TASK-" | wc -l)
echo "[$TIMESTAMP] 📊 Found $ACTIVE_COUNT active tasks"

# Simple autonomous analysis
IMPROVEMENTS_FOUND=0
TASKS_CREATED=0
TASKS_EXECUTED=0

# Check for quick wins (simple fixes, high impact)
echo "[$TIMESTAMP] 🔍 Checking for quick wins..."

# Check git status for uncommitted changes (indicates work in progress)
UNCOMMITTED=$(cd "$BB5_DIR" && git status --porcelain | wc -l)

if [ "$UNCOMMITTED" -gt 5 ]; then
    echo "[$TIMESTAMP] ✅ Found $UNCOMMITTED uncommitted changes - likely improvements in progress"
    echo "[$TIMESTAMP] 📊 System is active with ongoing work"
    echo "[$TIMESTAMP] ℹ️ No new improvements needed at this time"
    exit 0
fi

# Check for old completed tasks that might have issues (created >7 days ago)
echo "[$TIMESTAMP] 🔍 Checking completed tasks for issues..."

OLD_ISSUES=0
find "$BB5_DIR/5-project-memory/blackbox5/tasks/completed" -maxdepth 1 -type d -mtime +7 | while read -r dir && do
    if [ -f "$dir/task.md" ]; then
        ISSUE_COUNT=$((ISSUE_COUNT + 1))
        echo "[$TIMESTAMP] ⚠️  Found potential issue in $dir (completed >7 days ago)"
    done

if [ "$OLD_ISSUES" -gt 3 ]; then
    echo "[$TIMESTAMP] ✅ Found $OLD_ISSUES completed tasks that may need attention"
    
    # Create improvement task for reviewing old completed tasks
    REVIEW_ID="TASK-AUTO-$(date +%s)"
    REVIEW_DIR="$BB5_DIR/5-project-memory/blackbox5/tasks/active/$REVIEW_ID"
    mkdir -p "$REVIEW_DIR"
    
    cat > "$REVIEW_DIR/task.md" << 'TASKEOF'
# $REVIEW_ID: Review Old Completed Tasks

**Status:** in_progress
**Priority:** MEDIUM
**Type:** maintenance
**Category:** completed_tasks_review
**Created:** $TIMESTAMP
**Agent:** autonomous
**ROI Score:** 25

## Problem
Found $OLD_ISSUES completed tasks created more than 7 days ago. These may contain issues, outdated solutions, or need archiving.

## Current State
$OLD_ISSUES tasks in tasks/completed/ are >7 days old.

## Proposed Fix
Review each old completed task and:
1. If solution is still valid and in use, leave as-is
2. If solution is outdated or has issues, re-apply fixes
3. If task is no longer relevant, archive or delete
4. If better solution exists, replace with new approach

## Acceptance Criteria
- [ ] All $OLD_ISSUES old completed tasks reviewed
- [ ] Appropriate action taken (archive, delete, re-apply, or leave as-is)
- [ ] Tasks updated (archived if needed)
- [ ] Documentation updated with review findings
- [ ] No tasks left in ambiguous state

## Execution
1. List all old completed tasks (>7 days)
2. For each task, review task.md and any implementation
3. Determine appropriate action for each
4. Execute actions (archive, delete, or validate)
5. Update task status to "archived" if archived
6. Document findings in task.md
7. Commit changes to git

## Notes
Some tasks may be left as-is if still relevant.
Focus cleanup on truly obsolete or problematic tasks.
TASKEOF
    
    echo "[$TIMESTAMP] ✅ Created review task: $REVIEW_ID"
    TASKS_CREATED=$((TASKS_CREATED + 1))
    IMPROVEMENTS_FOUND=$((IMPROVEMENTS_FOUND + 1))
    
    exit 0
elif [ "$OLD_ISSUES" -gt 0 ]; then
    echo "[$TIMESTAMP] ✅ Created improvement task: $REVIEW_ID"
    TASKS_CREATED=$((TASKS_CREATED + 1))
    IMPROVEMENTS_FOUND=$((IMPROVEMENTS_FOUND + 1))
else
    echo "[$TIMESTAMP] ℹ️ No old completed tasks need review"
fi

# Summary
echo "[$TIMESTAMP] 📊 Summary:"
echo "[$TIMESTAMP]   - Tasks analyzed: $ACTIVE_COUNT"
echo "[$TIMESTAMP]   - Improvements found: $IMPROVEMENTS_FOUND"
echo "[$TIMESTAMP]   - Tasks created: $TASKS_CREATED"
echo "[$TIMESTAMP]   - Uncommitted changes: $UNCOMMITTED"

if [ "$IMPROVEMENTS_FOUND" -eq 0 ]; then
    if [ "$UNCOMMITTED" -eq 0 ]; then
        echo "[$TIMESTAMP] ℹ️ No improvements needed - system is healthy with ongoing work"
    else
        echo "[$TIMESTAMP] ✅ Improvement tasks created - system will continue work"
        echo "[$TIMESTAMP] ℹ️ Continuing with ongoing tasks and improvements"
fi

echo "[$TIMESTAMP] ✅ Autonomous cycle complete"
exit 0
