#!/bin/bash
TASKS_DIR=/opt/blackbox5/5-project-memory/blackbox5/.autonomous/tasks
tmpfile=$(mktemp)
find "$TASKS_DIR/active" -name "TASK-*.md" -type f > "$tmpfile" 2>/dev/null
echo "Found $(wc -l < "$tmpfile") task files"

while IFS= read -r task_file; do
  echo "Checking: $task_file"
  status_line=$(grep 'Status:' "$task_file" 2>/dev/null | grep -E '(pending|partial)' | head -1 || echo "")
  echo "  Status line: [$status_line]"
  status=$(echo "$status_line" | sed 's/.*:\s*//' | tr -d '[:space:]*' || echo "")
  echo "  Extracted: [$status]"
  if [ -n "$status" ]; then
    echo "  -> MATCH!"
  fi
done < "$tmpfile"
rm -f "$tmpfile"
