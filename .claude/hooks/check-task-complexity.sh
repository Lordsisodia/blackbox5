#!/bin/bash
#
# Blackbox5 Hook: Check Task Complexity
# Event: UserPromptSubmit
# Purpose: Break complex tasks into tractable pieces
#

set -euo pipefail

data=$(cat)
prompt=$(echo "$data" | jq -r '.prompt // empty')

# Count complexity indicators
and_count=$(echo "$prompt" | grep -oi " and " | wc -l)
clause_count=$(echo "$prompt" | grep -o "," | wc -l)
word_count=$(echo "$prompt" | wc -w)

# Check if task seems complex
complexity_score=$((and_count * 2 + clause_count))

if [[ $complexity_score -gt 5 ]] || [[ $word_count -gt 100 ]]; then
  cat << 'EOF'

# 📋 Task Complexity Check

This task appears complex. Consider breaking it down:

Suggested approach:
1. Identify the main goal
2. List sub-tasks (3-7 items)
3. Prioritize sub-tasks
4. Tackle one at a time

Would you like me to help break this down into smaller steps?

---
EOF
fi

echo "$prompt"
exit 0
