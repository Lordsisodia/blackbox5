#!/bin/bash
#
# Blackbox5 Hook: Auto-log Activity
# Event: PostToolUse
# Purpose: Complete audit trail of all work
#

set -euo pipefail

# Read input from Claude Code
data=$(cat)
tool_name=$(echo "$data" | jq -r '.tool_name // empty')
file_path=$(echo "$data" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || echo "")
session_id=$(echo "$data" | jq -r '.session_id // "unknown"')
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Only log Edit and Write operations
if [[ ! "$tool_name" =~ ^(Edit|Write)$ ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$file_path" ]]; then
  exit 0
fi

# Determine work log path
WORK_LOG="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/WORK-LOG.md"

# Ensure directory exists
mkdir -p "$(dirname "$WORK_LOG")"

# Append to work log
cat >> "$WORK_LOG" << EOF
- date: "$timestamp"
  source: "claude-code"
  type: "tool_use"
  tool: "$tool_name"
  file: "$file_path"
  session: "$session_id"
EOF

exit 0
