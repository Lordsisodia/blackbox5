#!/bin/bash
#
# Blackbox5 Hook: Detect Dependencies
# Event: UserPromptSubmit
# Purpose: Identify blockers before starting
#

set -euo pipefail

data=$(cat)
prompt=$(echo "$data" | jq -r '.prompt // empty')

# Dependency patterns
DEP_PATTERNS=(
  "needs [a-zA-Z]"
  "requires [a-zA-Z]"
  "after [a-zA-Z]"
  "depends on [a-zA-Z]"
  "waiting for [a-zA-Z]"
  "blocked by [a-zA-Z]"
)

found_deps=()
for pattern in "${DEP_PATTERNS[@]}"; do
  if echo "$prompt" | grep -qi "$pattern"; then
    # Extract the dependency
    dep=$(echo "$prompt" | grep -oi "$pattern" | sed 's/.*\(needs\|requires\|after\|depends on\|waiting for\|blocked by\) [a-zA-Z]*.*/\1/i' | head -1)
    found_deps+=("$dep")
  fi
done

if [[ ${#found_deps[@]} -gt 0 ]]; then
  cat << 'EOF'

# 🔗 Dependency Detection

I detected potential dependencies:
EOF

  for dep in "${found_deps[@]}"; do
    echo "  - $dep"
  done

  cat << 'EOF'

Before starting, verify:
- Are these dependencies satisfied?
- Are they in the right state?
- What blocks this task if they're not ready?

---
EOF
fi

echo "$prompt"
exit 0
