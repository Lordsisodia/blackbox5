#!/bin/bash
#
# Blackbox5 Hook: Detect Assumptions
# Event: UserPromptSubmit
# Purpose: Question implicit assumptions
#

set -euo pipefail

# Read input from Claude Code
data=$(cat)
prompt=$(echo "$data" | jq -r '.prompt // empty')

# Assumption indicators
ASSUMPTION_PATTERNS=(
  "obviously"
  "clearly"
  "should be"
  "everyone knows"
  "of course"
  "naturally"
  "it goes without saying"
)

# Check for assumptions
found_assumptions=()
for pattern in "${ASSUMPTION_PATTERNS[@]}"; do
  if echo "$prompt" | grep -qi "$pattern"; then
    found_assumptions+=("$pattern")
  fi
done

# If assumptions found, inject questions
if [[ ${#found_assumptions[@]} -gt 0 ]]; then
  cat << 'EOF'

# 🔍 Assumption Detection

I noticed some phrases that might indicate implicit assumptions:
EOF

  for assumption in "${found_assumptions[@]}"; do
    echo "  - \"$assumption\""
  done

  cat << 'EOF'

Before proceeding, let's question these:
- What evidence supports this assumption?
- What would change if this assumption were wrong?
- Is this assumption based on data or intuition?
- Should we validate this assumption first?

---
EOF
fi

# Always output the original prompt
echo "$prompt"

exit 0
