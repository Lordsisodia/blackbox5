#!/bin/bash
#
# Blackbox5 Hook: Detect Patterns
# Event: SessionEnd
# Purpose: Spot systemic issues
#

set -euo pipefail

data=$(cat)
session_id=$(echo "$data" | jq -r '.session_id // "unknown"')

WORK_LOG="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/WORK-LOG.md"

if [[ ! -f "$WORK_LOG" ]]; then
  exit 0
fi

# Find files edited >3 times in this session
frequently_edited=$(grep "session: $session_id" "$WORK_LOG" 2>/dev/null | \
  grep -o 'file: "[^"]*"' | cut -d'"' -f2 | sort | uniq -c | sort -rn | \
  awk '$1 > 3 {print $2}')

if [[ -n "$frequently_edited" ]]; then
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # Log to pattern detection file
  PATTERN_FILE="${BLACKBOX5_MEMORY_PATH:-./5-project-memory/siso-internal}/operations/pattern-detection.txt"
  mkdir -p "$(dirname "$PATTERN_FILE")"

  echo "[$timestamp] Session $session_id:" >> "$PATTERN_FILE"
  echo "  Frequently edited files:" >> "$PATTERN_FILE"
  echo "$frequently_edited" >> "$PATTERN_FILE"
  echo "" >> "$PATTERN_FILE"
fi

exit 0
