#!/bin/bash
#
# Blackbox5 Hook: Detect Technical Debt
# Event: PostToolUse (Edit/Write)
# Purpose: Track debt explicitly
#

set -euo pipefail

data=$(cat)
tool_name=$(echo "$data" | jq -r '.tool_name // empty')
file_path=$(echo "$data" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || echo "")

# Only check Edit/Write operations
if [[ ! "$tool_name" =~ ^(Edit|Write)$ ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$file_path" ]] || [[ ! -f "$file_path" ]]; then
  exit 0
fi

# Look for debt indicators
debt_found=false
debt_items=()

# Check for TODO/FIXME/HACK comments
while IFS= read -r line; do
  if [[ "$line" =~ (TODO|FIXME|HACK|XXX) ]]; then
    debt_found=true
    debt_items+=("  $line")
  fi
done < "$file_path"

# Track file edit frequency
DEBT_TRACKER="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/operations/technical-debt.txt"

if [[ "$debt_found" == "true" ]]; then
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$timestamp] $file_path" >> "$DEBT_TRACKER"
  echo "  Debt markers found: ${#debt_items[@]}" >> "$DEBT_TRACKER"

  # Only show if significant debt
  if [[ ${#debt_items[@]} -gt 2 ]]; then
    echo ""
    echo "🏗️  Technical Debt Detected"
    echo ""
    echo "File: $file_path"
    echo "Debt markers: ${#debt_items[@]}"
    echo ""
    echo "Consider addressing in future work. Track at: $DEBT_TRACKER"
    echo ""
  fi
fi

exit 0
