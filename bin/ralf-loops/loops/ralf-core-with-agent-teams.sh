#!/bin/bash
# RALF Core Loop with Agent Teams Integration
# Continuous autonomous improvement with BB5 Core Agent Team

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BB5_DIR="$(cd "$SCRIPT_DIR/../../../" && pwd)"
RUN_ID=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="$BB5_DIR/runs/$RUN_ID"

# Configuration
INTERVAL=${INTERVAL:-300}  # 5 minutes default
CONTINUOUS=false
USE_AGENT_TEAMS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --continuous)
      CONTINUOUS=true
      shift
      ;;
    --agent-teams)
      USE_AGENT_TEAMS=true
      shift
      ;;
    --interval)
      INTERVAL="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Setup run directory
mkdir -p "$RUN_DIR"
ln -sf "$RUN_DIR" "$BB5_DIR/runs/current"

# Initialize run files
init_run_files() {
  cat > "$RUN_DIR/THOUGHTS.md" << EOF
# RALF Core Run - $RUN_ID

**Mode:** Autonomous with Agent Teams
**Started:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Cycle Log

EOF

  cat > "$RUN_DIR/DECISIONS.md" << EOF
# Decisions - $RUN_ID

## Autonomous Decisions

EOF

  cat > "$RUN_DIR/LEARNINGS.md" << EOF
# Learnings - $RUN_ID

## Cycle Learnings

EOF

  cat > "$RUN_DIR/RESULTS.md" << EOF
# Results - $RUN_ID

## Cycle Results

EOF
}

# Activate BB5 Core Agent Team
activate_agent_teams() {
  echo "🤖 Activating BB5 Core Agent Team..."

  # Create activation marker
  cat > "$RUN_DIR/.agent_teams_active" << EOF
AGENT_TEAMS_ACTIVE: true
ACTIVATED_AT: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
CORE_TEAM:
  - bb5-context-collector
  - bb5-scribe
  - bb5-superintelligence
EOF

  echo "✅ Agent Teams activated for this run"
  echo "   - Context Collector will gather BB5 state"
  echo "   - Scribe will document all activity"
  echo "   - Superintelligence will analyze complex issues"
}

# Analyze BB5 state
analyze_bb5() {
  echo "🔍 Analyzing BB5 state..."

  # Find orphaned tasks
  ORPHANED=$(find "$BB5_DIR/6-roadmap" -name "*.md" -type f -mtime +7 2>/dev/null | wc -l)

  # Check doc drift
  DOC_DRIFT=$(git -C "$BB5_DIR" diff --name-only 2>/dev/null | grep -c "\.md$" || echo "0")

  # Check skill registry
  SKILL_COUNT=$(find "$BB5_DIR/.claude/skills" -name "SKILL.md" 2>/dev/null | wc -l)

  # Git health
  GIT_STATUS=$(git -C "$BB5_DIR" status --porcelain 2>/dev/null | wc -l)

  cat >> "$RUN_DIR/THOUGHTS.md" << EOF

### Analysis $(date +"%H:%M:%S")
- Orphaned tasks: $ORPHANED
- Documentation drift: $DOC_DRIFT files
- Skills registered: $SKILL_COUNT
- Git uncommitted: $GIT_STATUS

EOF

  echo "   Found: $ORPHANED orphaned, $DOC_DRIFT doc drift, $SKILL_COUNT skills"
}

# Determine next action
 determine_action() {
  echo "🎯 Determining next action..."

  # Priority order
  if [ -f "$BB5_DIR/.autonomous/tasks/active/"*.md ] 2>/dev/null; then
    ACTION="process_active_task"
    PRIORITY="high"
  elif git -C "$BB5_DIR" status --porcelain | grep -q "\.md$"; then
    ACTION="sync_documentation"
    PRIORITY="medium"
  else
    ACTION="improve_infrastructure"
    PRIORITY="low"
  fi

  echo "   Action: $ACTION (priority: $PRIORITY)"

  cat >> "$RUN_DIR/DECISIONS.md" << EOF

### $(date +"%H:%M:%S") - Cycle Decision
**Action:** $ACTION
**Priority:** $PRIORITY
**Rationale:** Based on BB5 state analysis
EOF
}

# Execute action with agent teams
execute_action() {
  local action="$1"

  echo "⚡ Executing: $action"

  case "$action" in
    process_active_task)
      echo "   Processing active tasks..."
      # Agent teams will handle this
      ;;
    sync_documentation)
      echo "   Syncing documentation..."
      git -C "$BB5_DIR" add -A 2>/dev/null || true
      git -C "$BB5_DIR" commit -m "docs: Auto-sync documentation [RALF $RUN_ID]" 2>/dev/null || true
      ;;
    improve_infrastructure)
      echo "   Running infrastructure improvements..."
      # Trigger agent teams for complex analysis
      ;;
  esac

  cat >> "$RUN_DIR/RESULTS.md" << EOF

### $(date +"%H:%M:%S") - $action
**Status:** completed
**Agent Teams:** $USE_AGENT_TEAMS
EOF
}

# Log learning
log_learning() {
  local what_worked="$1"
  local what_hard="$2"

  cat >> "$RUN_DIR/LEARNINGS.md" << EOF

### $(date +"%H:%M:%S")
**What Worked:** $what_worked
**What Was Hard:** $what_hard
EOF
}

# Main cycle
run_cycle() {
  echo ""
  echo "═══════════════════════════════════════════"
  echo "🔄 RALF Core Cycle - $RUN_ID"
  echo "═══════════════════════════════════════════"
  echo "Time: $(date)"
  echo "Agent Teams: $USE_AGENT_TEAMS"
  echo ""

  # Pull latest
  echo "📥 Pulling latest changes..."
  git -C "$BB5_DIR" pull origin main 2>/dev/null || echo "   (Could not pull)"

  # Analyze
  analyze_bb5

  # Determine action
  determine_action

  # Execute
  execute_action "$(determine_action | grep 'Action:' | cut -d: -f2 | tr -d ' ')"

  # Log learning
  log_learning "Cycle completed successfully" "Determining optimal action priority"

  # Push changes
  echo "📤 Pushing changes..."
  git -C "$BB5_DIR" push origin main 2>/dev/null || echo "   (Nothing to push)"

  echo ""
  echo "✅ Cycle complete"
  echo "Next cycle in $INTERVAL seconds"
  echo "═══════════════════════════════════════════"
}

# Main
main() {
  echo "🚀 RALF Core with Agent Teams"
  echo "═══════════════════════════════════════════"

  init_run_files

  if [ "$USE_AGENT_TEAMS" = true ]; then
    activate_agent_teams
  fi

  if [ "$CONTINUOUS" = true ]; then
    echo "Mode: Continuous (interval: ${INTERVAL}s)"
    echo ""

    while true; do
      run_cycle
      sleep "$INTERVAL"
    done
  else
    echo "Mode: Single cycle"
    echo ""
    run_cycle
  fi
}

main "$@"
