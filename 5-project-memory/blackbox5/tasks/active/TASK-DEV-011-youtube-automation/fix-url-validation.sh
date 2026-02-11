#!/bin/bash
# Fix: Add URL validation to YouTube automation
# Prevents "404 url.not_found" errors when task has no URL

cd /opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-DEV-011-youtube-automation/

# Check if task has URL requirement
if grep -q "URL:" task.md > /dev/null 2>&1; then
    echo "Task does not require URL - skip validation"
    exit 0
fi

# Add URL validation to task requirements
sed -i '/Acceptance Criteria/a) \[/a-z]/URL:/)' task.md >> task.md.tmp
mv task.md.tmp task.md

echo "Added URL validation requirement to task"
exit 0
