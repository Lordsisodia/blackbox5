#!/bin/bash
task_file=/opt/blackbox5/5-project-memory/blackbox5/.autonomous/tasks/active/IMPROVING-V2-HOOKS/tasks/TASK-20260203171821-enhance-session-start.md
echo "Testing grep on: $task_file"
grep -E '^\*\*Status:' "$task_file"
echo "Exit code: $?"
