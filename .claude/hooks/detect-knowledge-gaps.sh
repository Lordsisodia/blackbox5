#!/bin/bash
#
# Blackbox5 Hook: Detect Knowledge Gaps
# Event: UserPromptSubmit
# Purpose: Identify learning needs before proceeding
#

set -euo pipefail

data=$(cat)
prompt=$(echo "$data" | jq -r '.prompt // empty')

# Uncertainty indicators
UNCERTAINTY_PATTERNS=(
  "i think"
  "probably"
  "should work"
  "might be"
  "i believe"
  "i guess"
  "not sure"
  "familiar with"
  "need to understand"
)

found_gaps=()
for pattern in "${UNCERTAINTY_PATTERNS[@]}"; do
  if echo "$prompt" | grep -qi "$pattern"; then
    found_gaps+=("$pattern")
  fi
done

# Also check for unfamiliar technical terms
unfamiliar_terms=(
  "never used"
  "not familiar with"
  "new to"
  "learning"
  "figure out"
)

for pattern in "${unfamiliar_terms[@]}"; do
  if echo "$prompt" | grep -qi "$pattern"; then
    found_gaps+=("unfamiliar_domain")
  fi
done

if [[ ${#found_gaps[@]} -gt 0 ]]; then
  cat << 'EOF'

# 🧠 Knowledge Gap Detection

I detected some uncertainty in your request. This suggests a learning gap.

Before implementing, consider:
1. What do we need to learn first?
2. What research would reduce uncertainty?
3. Can we validate assumptions before building?

Options:
- "Research [topic]" - Deep dive into unfamiliar area
- "Spike [topic]" - Time-boxed exploration
- "Prototype [feature]" - Learn by building

Proceed when ready, but consider investing in understanding first.

---
EOF
fi

echo "$prompt"
exit 0
