#!/bin/bash
# RALF Redis Reporter - Publishes status to Redis for remote monitoring

BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
RUNS_DIR="$BB5_DIR/5-project-memory/blackbox5/.autonomous/runs"
LOG_FILE="$BB5_DIR/.autonomous/logs/ralf-core.log"
REDIS_KEY="ralf:status"

while true; do
    STATUS_JSON=$(cat <<EOF
{
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "ralf_running": $(pgrep -f "ralf-core.sh" > /dev/null && echo "true" || echo "false"),
    "claude_running": $(pgrep -x "claude" > /dev/null && echo "true" || echo "false"),
    "current_task": "$(ls -td "$RUNS_DIR"/run-* 2>/dev/null | head -1 | xargs basename 2>/dev/null | sed 's/run-[0-9]*_[0-9]*-//' || echo 'none')",
    "pending_tasks": $(find "$BB5_DIR/5-project-memory/blackbox5/.autonomous/tasks/active" -name "TASK-*.md" -exec grep -l "Status: pending\|Status: partial" {} \; 2>/dev/null | wc -l),
    "latest_log": "$(tail -5 "$LOG_FILE" 2>/dev/null | tr '\n' '|' | sed 's/|/\\n/g' | tail -c 500)"
}
EOF
)

    redis-cli SET "$REDIS_KEY" "$STATUS_JSON" EX 60 > /dev/null
    sleep 10
done
