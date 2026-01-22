#!/bin/bash
#
# Blackbox5 Hook: First Principles Triggering
# Event: UserPromptSubmit
# Purpose: Inject first principles framework for complex problems
#

set -euo pipefail

# Read input from Claude Code
data=$(cat)
prompt=$(echo "$data" | jq -r '.prompt // empty')

# First principles triggers
FP_KEYWORDS=(
  "architecture"
  "design"
  "approach"
  "how to"
  "best way to"
  "should we"
  "strategy"
  "plan for"
)

# Check if any trigger is present
trigger_detected=false
for keyword in "${FP_KEYWORDS[@]}"; do
  if echo "$prompt" | grep -qi "$keyword"; then
    trigger_detected=true
    break
  fi
done

# If trigger detected, inject first principles framework
if [[ "$trigger_detected" == "true" ]]; then
  cat << 'EOF'

# 🧠 First Principles Analysis

Before proceeding, let's apply first principles thinking:

## 1. Question the Question
- What problem are we ACTUALLY trying to solve?
- What is the fundamental goal?
- Are we solving the right problem?

## 2. Identify Assumptions
- What are we assuming to be true?
- Which assumptions are untested?
- What would change if assumptions were wrong?

## 3. Break Down to Fundamentals
- What are the core components?
- What are the essential properties?
- What are the true constraints?

## 4. Build Up from First Principles
- Given the fundamentals, what MUST be true?
- What solutions emerge from the ground up?
- What alternatives haven't we considered?

---

Proceeding with your request, grounded in first principles:

EOF
fi

# Always output the original prompt
echo "$prompt"

exit 0
