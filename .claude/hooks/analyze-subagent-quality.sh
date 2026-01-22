#!/bin/bash
#
# Blackbox5 Hook: Analyze Subagent Quality
# Event: SubagentStop
# Purpose: Quality gate for autonomous work
#

set -euo pipefail

data=$(cat)
agent_type=$(echo "$data" | jq -r '.agent_type // "unknown"')
result=$(echo "$data" | jq -r '.result // ""')

# Skip if no result
if [[ -z "$result" ]]; then
  exit 0
fi

# Simple quality metrics
word_count=$(echo "$result" | wc -w)
line_count=$(echo "$result" | wc -l)

# Calculate score (0-100)
score=100

# Penalize very short responses
if [[ $word_count -lt 10 ]]; then
  score=$((score - 50))
elif [[ $word_count -lt 50 ]]; then
  score=$((score - 20))
fi

# Penalize single-line responses
if [[ $line_count -lt 2 ]]; then
  score=$((score - 30))
fi

# Log results
QUALITY_LOG="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/operations/agent-quality.txt"
mkdir -p "$(dirname "$QUALITY_LOG")"

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[$timestamp] Agent: $agent_type | Words: $word_count | Lines: $line_count | Score: $score/100" >> "$QUALITY_LOG"

# Warn if low quality
if [[ $score -lt 70 ]]; then
  echo ""
  echo "📊 Subagent Quality Check"
  echo ""
  echo "Agent: $agent_type"
  echo "Score: $score/100"
  echo ""
  echo "This subagent result may need review."
  echo ""
fi

exit 0
