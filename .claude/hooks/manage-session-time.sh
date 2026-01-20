#!/bin/bash
#
# Blackbox5 Hook: Manage Session Time
# Event: SessionStart
# Purpose: Prevent fatigue-induced mistakes
#

set -euo pipefail

# Session timeout (default 4 hours)
TIMEOUT=${BLACKBOX5_SESSION_TIMEOUT:-14400}

# Track session start time if not already tracked
SESSION_START_FILE="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/.session_start"

if [[ ! -f "$SESSION_START_FILE" ]]; then
  date +%s > "$SESSION_START_FILE"
fi

# Check session duration
if [[ -f "$SESSION_START_FILE" ]]; then
  start_time=$(cat "$SESSION_START_FILE")
  current_time=$(date +%s)
  elapsed=$((current_time - start_time))

  # Warn at 2 hours (7200 seconds)
  if [[ $elapsed -gt 7200 ]]; then
    hours=$((elapsed / 3600))
    echo ""
    echo "⏰ Session Time Warning"
    echo ""
    echo "You've been working for ${hours} hours."
    echo ""
    echo "Consider:"
    echo "  - Taking a break to refresh"
    echo "  - Summarizing progress so far"
    echo "  - Starting a fresh session later"
    echo ""

    # Hard stop at 4 hours
    if [[ $elapsed -gt $TIMEOUT ]]; then
      echo "❌ Session Timeout"
      echo ""
      echo "Maximum session duration reached."
      echo "Please start a fresh session."
      echo ""
      exit 2  # Block continuation
    fi
  fi
fi

exit 0
