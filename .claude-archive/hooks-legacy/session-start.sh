#!/bin/bash
# Session Start Hook: Auto-spawn BB5 Agent Teams
# This hook runs at the start of every Claude session
# It ensures BB5 memory logging and activates core sub-agents

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BB5_DIR="$(cd "$SCRIPT_DIR/../../../" && pwd)"

# Log to events
echo "{
  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
  \"event\": \"session_start_agent_teams\",
  \"hook\": \"session-start-agent-teams.sh\",
  \"bb5_dir\": \"$BB5_DIR\"
}" >> "$BB5_DIR/.autonomous/agents/communications/events.yaml"

# Ensure BB5 memory structure exists
mkdir -p "$BB5_DIR/.autonomous/memory/data"
mkdir -p "$BB5_DIR/.autonomous/tasks/active"
mkdir -p "$BB5_DIR/.autonomous/tasks/completed"
mkdir -p "$BB5_DIR/runs/current"

# Create current run directory with timestamp
RUN_ID=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="$BB5_DIR/runs/$RUN_ID"
mkdir -p "$RUN_DIR"

# Link as current
rm -f "$BB5_DIR/runs/current"
ln -s "$RUN_DIR" "$BB5_DIR/runs/current"

# Initialize run documentation files
touch "$RUN_DIR/THOUGHTS.md"
touch "$RUN_DIR/DECISIONS.md"
touch "$RUN_DIR/LEARNINGS.md"
touch "$RUN_DIR/RESULTS.md"
touch "$RUN_DIR/ASSUMPTIONS.md"

# Add run header
cat > "$RUN_DIR/THOUGHTS.md" << EOF
# Run $RUN_ID - THOUGHTS

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Session Type:** $(echo "$CLAUDE_CODE_AGENT_TYPE" | tr '[:lower:]' '[:upper:]')

## Initial Context

EOF

cat > "$RUN_DIR/DECISIONS.md" << EOF
# Run $RUN_ID - DECISIONS

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Decisions Made

EOF

cat > "$RUN_DIR/LEARNINGS.md" << EOF
# Run $RUN_ID - LEARNINGS

**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## What Worked Well

## What Was Harder Than Expected

## What Would We Do Differently

## Patterns Detected

EOF

# Update agent state
if [ -f "$BB5_DIR/.autonomous/agents/communications/agent-state.yaml" ]; then
  # Update existing state
  sed -i.bak "s/last_session:.*/last_session: $RUN_ID/" "$BB5_DIR/.autonomous/agents/communications/agent-state.yaml"
  sed -i.bak "s/status:.*/status: ACTIVE/" "$BB5_DIR/.autonomous/agents/communications/agent-state.yaml"
  rm -f "$BB5_DIR/.autonomous/agents/communications/agent-state.yaml.bak"
else
  # Create new state
  cat > "$BB5_DIR/.autonomous/agents/communications/agent-state.yaml" << EOF
agent_id: $(hostname)-$$
agent_type: ${CLAUDE_CODE_AGENT_TYPE:-unknown}
status: ACTIVE
started: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
last_session: $RUN_ID
bb5_version: "5.0"
EOF
fi

echo "✓ BB5 Agent Teams session initialized"
echo "✓ Run directory: $RUN_DIR"
echo "✓ Memory logging active"
