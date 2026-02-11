#!/bin/bash
#
# BlackBox5 Autonomous Agent Team Runner
# Runs Scout → Builder → Auditor every 30 minutes
#

set -e

BB5_DIR="/opt/blackbox5"
SHARED_STATE="$BB5_DIR/.autonomous/shared-state.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Ensure directories exist
mkdir -p "$BB5_DIR/.autonomous/agent-roles"
mkdir -p "$(dirname "$SHARED_STATE")"

# Initialize shared state if doesn't exist
if [ ! -f "$SHARED_STATE" ]; then
    cat > "$SHARED_STATE" << 'EOF'
{
  "initialized": "$TIMESTAMP",
  "last_scout_run": null,
  "last_builder_run": null,
  "last_auditor_run": null,
  "tasks_identified": [],
  "tasks_completed": [],
  "issues_flagged": []
}
EOF
fi

echo "[$TIMESTAMP] 🚀 Starting Agent Team"
echo "[$TIMESTAMP] Reading shared state from $SHARED_STATE"

# ============================================
# AGENT 1: SCOUT - Find High-ROI Tasks
# ============================================
echo "[$TIMESTAMP] 🔍 Agent 1: Scout - Finding high-ROI improvements..."

SCOUT_ROLE="$BB5_DIR/.autonomous/agent-roles/scout-agent.md"
SCOUT_TASK=$(cat "$SCOUT_ROLE")

# Spawn Scout Agent
openclaw sessions_spawn \
  --task "$SCOUT_TASK" \
  --label "scout-agent" \
  --cleanup delete \
  --model zai/glm-4.7 \
  --thinking high

echo "[$TIMESTAMP] Scout agent spawned, waiting for completion..."
sleep 5  # Give scout time to work

# ============================================
# AGENT 2: BUILDER - Execute High-ROI Tasks
# ============================================
echo "[$TIMESTAMP] 🔧 Agent 2: Builder - Executing high-ROI tasks..."

BUILDER_ROLE="$BB5_DIR/.autonomous/agent-roles/builder-agent.md"
BUILDER_TASK=$(cat "$BUILDER_ROLE")

# Spawn Builder Agent
openclaw sessions_spawn \
  --task "$BUILDER_TASK" \
  --label "builder-agent" \
  --cleanup delete \
  --model zai/glm-4.7 \
  --thinking high

echo "[$TIMESTAMP] Builder agent spawned, waiting for completion..."
sleep 10  # Give builder more time

# ============================================
# AGENT 3: AUDITOR - Validate Work
# ============================================
echo "[$TIMESTAMP] 📊 Agent 3: Auditor - Validating work quality..."

AUDITOR_ROLE="$BB5_DIR/.autonomous/agent-roles/auditor-agent.md"
AUDITOR_TASK=$(cat "$AUDITOR_ROLE")

# Spawn Auditor Agent
openclaw sessions_spawn \
  --task "$AUDITOR_TASK" \
  --label "auditor-agent" \
  --cleanup delete \
  --model zai/glm-4.7 \
  --thinking high

echo "[$TIMESTAMP] Auditor agent spawned, waiting for completion..."
sleep 5  # Give auditor time to review

# ============================================
# FINAL REPORT
# ============================================
echo "[$TIMESTAMP] ✅ Agent Team Run Complete"
echo "[$TIMESTAMP] Summary:"

# Read final shared state
if [ -f "$SHARED_STATE" ]; then
    echo "[$TIMESTAMP] Shared State:"
    cat "$SHARED_STATE"
else
    echo "[$TIMESTAMP] ⚠️  No shared state file found"
fi

echo "[$TIMESTAMP] 📊 Quality Metrics:"
if [ -f "$BB5_DIR/.autonomous/quality-metrics.json" ]; then
    cat "$BB5_DIR/.autonomous/quality-metrics.json"
else
    echo "[$TIMESTAMP] No quality metrics yet"
fi

exit 0
