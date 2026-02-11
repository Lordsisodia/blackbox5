#!/bin/bash
# Post Message Hook: Spawn BB5 Agent Teams for complex tasks
# This hook runs after user messages to auto-activate agent teams

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BB5_DIR="$(cd "$SCRIPT_DIR/../../../" && pwd)"
RUN_DIR="$BB5_DIR/runs/current"

# Read the user message from stdin (if provided)
USER_MESSAGE="${1:-}"

# Keywords that trigger agent team activation
TRIGGER_KEYWORDS=(
  "architecture"
  "design"
  "refactor"
  "optimize"
  "strategy"
  "complex"
  "integrate"
  "implement"
  "create"
  "build"
  "analyze"
  "research"
  "improve"
  "fix"
)

# Check if message contains trigger keywords
SHOULD_ACTIVATE=false
for keyword in "${TRIGGER_KEYWORDS[@]}"; do
  if echo "$USER_MESSAGE" | grep -qi "$keyword"; then
    SHOULD_ACTIVATE=true
    break
  fi
done

# Log the check
echo "{
  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
  \"event\": \"post_message_check\",
  \"hook\": \"post-message-agent-teams.sh\",
  \"should_activate\": $SHOULD_ACTIVATE,
  \"message_preview\": \"$(echo "$USER_MESSAGE" | cut -c1-100)\"
}" >> "$BB5_DIR/.autonomous/agents/communications/events.yaml"

# If should activate, create agent team instruction
if [ "$SHOULD_ACTIVATE" = true ]; then
  # Create agent team activation marker
  cat > "$RUN_DIR/.agent_teams_activated" << EOF
AGENT_TEAMS_ACTIVATED: true
TRIGGER: "$USER_MESSAGE"
TIMESTAMP: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

CORE_TEAM:
  - superintelligence: Activate 7-dimension analysis
  - context-collector: Gather BB5 context
  - scribe: Document all decisions and learnings

INSTRUCTIONS:
  1. Spawn bb5-context-collector to scan BB5 state
  2. Spawn bb5-superintelligence for complex analysis
  3. Ensure bb5-scribe is active for memory logging
  4. All outputs go to: $RUN_DIR/
EOF

  echo "✓ Agent Teams activation prepared"
  echo "✓ Core team: superintelligence, context-collector, scribe"
fi

exit 0
