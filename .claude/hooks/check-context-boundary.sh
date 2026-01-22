#!/bin/bash
#
# Blackbox5 Hook: Check Context Boundary
# Event: PreToolUse
# Purpose: Prevent context overflow failures
#

set -euo pipefail

# Read input from Claude Code
data=$(cat)
session_id=$(echo "$data" | jq -r '.session_id // "unknown"')

# Context threshold (default 80%)
THRESHOLD=${BLACKBOX5_CONTEXT_THRESHOLD:-80}

# For now, we'll estimate context based on WORK-LOG.md size
# In production, this would call Claude Code API to get actual context usage
WORK_LOG="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/WORK-LOG.md"

if [[ -f "$WORK_LOG" ]]; then
  # Rough heuristic: each line ≈ 100 tokens
  # This is not accurate but provides a warning
  line_count=$(wc -l < "$WORK_LOG" 2>/dev/null || echo "0")
  estimated_tokens=$((line_count * 100))

  # Assume 200K token context window
  context_usage=$((estimated_tokens * 100 / 200000))

  if [[ $context_usage -gt $THRESHOLD ]]; then
    echo ""
    echo "⚠️  Context Usage Warning"
    echo "Current context usage: ~${context_usage}% (estimated)"
    echo ""
    echo "Recommendations:"
    echo "  1. Run /compact to summarize older conversation"
    echo "  2. Start a new session with /clear"
    echo "  3. Use subagents for exploration to save context"
    echo ""

    # Hard block at 95%
    if [[ $context_usage -gt 95 ]]; then
      echo "❌ Context Critical: At capacity. Please compact before continuing."
      echo ""
      exit 2  # Block the operation
    fi
  fi
fi

exit 0
