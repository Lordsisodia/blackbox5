#!/bin/bash
#
# Blackbox5 Hook: Capture Decisions
# Event: PostToolUse (Write operations)
# Purpose: Record decision rationale automatically
#

set -euo pipefail

# Read input from Claude Code
data=$(cat)
tool_name=$(echo "$data" | jq -r '.tool_name // empty')
file_path=$(echo "$data" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || echo "")

# Only check Write operations
if [[ "$tool_name" != "Write" ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$file_path" ]]; then
  exit 0
fi

# Decision file patterns
DECISION_PATTERNS=(
  "decision"
  "adr"
  "architecture"
  "decision-record"
  "DECISION"
)

# Check if file matches decision pattern
is_decision=false
for pattern in "${DECISION_PATTERNS[@]}"; do
  if [[ "$file_path" == *"$pattern"* ]]; then
    is_decision=true
    break
  fi
done

# If it's a decision file, ensure it has proper structure
if [[ "$is_decision" == "true" ]]; then
  # Check if file has required sections
  if [[ -f "$file_path" ]]; then
    has_context=$(grep -q "## Context" "$file_path" 2>/dev/null && echo "yes" || echo "no")
    has_decision=$(grep -q "## Decision" "$file_path" 2>/dev/null && echo "yes" || echo "no")
    has_rationale=$(grep -q "## Rationale" "$file_path" 2>/dev/null && echo "yes" || echo "no")

    # If missing sections, add reminder
    if [[ "$has_context" == "no" ]] || [[ "$has_decision" == "no" ]] || [[ "$has_rationale" == "no" ]]; then
      echo ""
      echo "⚠️  Decision File Reminder"
      echo "This file appears to be a decision record. Ensure it includes:"
      echo "  - ## Context: Background and problem statement"
      echo "  - ## Decision: What was decided"
      echo "  - ## Rationale: Why this decision was made"
      echo "  - ## Alternatives: What else was considered"
      echo "  - ## Consequences: What this means"
      echo ""
    fi
  fi
fi

# Also log to decisions index
if [[ "$is_decision" == "true" ]]; then
  DECISIONS_INDEX="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/decisions/INDEX.md"
  mkdir -p "$(dirname "$DECISIONS_INDEX")"

  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "- [$timestamp] $file_path" >> "$DECISIONS_INDEX"
fi

exit 0
