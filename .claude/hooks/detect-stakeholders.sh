#!/bin/bash
#
# Blackbox5 Hook: Detect Stakeholders
# Event: PostToolUse (Write operations)
# Purpose: Right people are informed
#

set -euo pipefail

data=$(cat)
tool_name=$(echo "$data" | jq -r '.tool_name // empty')
file_path=$(echo "$data" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || echo "")

# Only check Write operations
if [[ "$tool_name" != "Write" ]]; then
  exit 0
fi

# Stakeholder mappings
declare -A stakeholder_map
stakeholder_map["decisions/"]="team"
stakeholder_map["api/"]="api-consumers"
stakeholder_map["schema/"]="frontend-team"
stakeholder_map["README.md"]="users"
stakeholder_map["CHANGELOG.md"]="users"

# Check if file matches any stakeholder category
for pattern in "${!stakeholder_map[@]}"; do
  if [[ "$file_path" == *"$pattern"* ]]; then
    stakeholder="${stakeholder_map[$pattern]}"
    echo ""
    echo "👥 Stakeholder Notification"
    echo ""
    echo "This change may affect: $stakeholder"
    echo ""
    echo "Consider:"
    echo "  - Notifying relevant stakeholders"
    echo "  - Updating communication channels"
    echo "  - Documenting breaking changes"
    echo ""
    break
  fi
done

exit 0
