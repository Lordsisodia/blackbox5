#!/bin/bash
#
# Blackbox5 Hook: Check Reversibility
# Event: PreToolUse (Edit/Delete operations)
# Purpose: Safe experimentation
#

set -euo pipefail

data=$(cat)
tool_name=$(echo "$data" | jq -r '.tool_name // empty')
tool_input=$(echo "$data" | jq -r '.tool_input // empty')

# Check for potentially irreversible operations
risky_patterns=(
  "rm -rf"
  "delete.*force"
  "drop.*table"
  "truncate"
)

is_risky=false
for pattern in "${risky_patterns[@]}"; do
  if echo "$tool_input" | grep -qi "$pattern"; then
    is_risky=true
    break
  fi
done

if [[ "$is_risky" == "true" ]]; then
  echo ""
  echo "⚠️  Reversibility Check"
  echo ""
  echo "This operation appears difficult to reverse."
  echo ""
  echo "Before proceeding, consider:"
  echo "  1. Create a backup branch:"
  echo "     git checkout -b backup/$(date +%s)"
  echo "  2. Confirm you really want to do this"
  echo "  3. Ensure you have a recent backup"
  echo ""
  echo "Continue? (Claude will ask for confirmation)"
  echo ""
fi

exit 0
