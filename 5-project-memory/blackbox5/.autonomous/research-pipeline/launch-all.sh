#!/bin/bash
# Launch all 6 Research Pipeline Agents

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================"
echo "Research Pipeline Launcher"
echo "================================"
echo ""
echo "This will launch 6 agents in parallel:"
echo "  - Scout Worker"
echo "  - Scout Validator"
echo "  - Analyst Worker"
echo "  - Analyst Validator"
echo "  - Planner Worker"
echo "  - Planner Validator"
echo ""
echo "Each agent needs its own terminal."
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

echo ""
echo "Launching agents..."
echo ""

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs/launcher"

# Launch each agent in background
echo "[1/6] Starting Scout Worker..."
"$SCRIPT_DIR/launch-scout-worker.sh" > "$SCRIPT_DIR/logs/launcher/scout-worker.log" 2>&1 &
SCOUT_WORKER_PID=$!
echo "        PID: $SCOUT_WORKER_PID"

echo "[2/6] Starting Scout Validator..."
"$SCRIPT_DIR/launch-scout-validator.sh" > "$SCRIPT_DIR/logs/launcher/scout-validator.log" 2>&1 &
SCOUT_VALIDATOR_PID=$!
echo "        PID: $SCOUT_VALIDATOR_PID"

echo "[3/6] Starting Analyst Worker..."
"$SCRIPT_DIR/launch-analyst-worker.sh" > "$SCRIPT_DIR/logs/launcher/analyst-worker.log" 2>&1 &
ANALYST_WORKER_PID=$!
echo "        PID: $ANALYST_WORKER_PID"

echo "[4/6] Starting Analyst Validator..."
"$SCRIPT_DIR/launch-analyst-validator.sh" > "$SCRIPT_DIR/logs/launcher/analyst-validator.log" 2>&1 &
ANALYST_VALIDATOR_PID=$!
echo "        PID: $ANALYST_VALIDATOR_PID"

echo "[5/6] Starting Planner Worker..."
"$SCRIPT_DIR/launch-planner-worker.sh" > "$SCRIPT_DIR/logs/launcher/planner-worker.log" 2>&1 &
PLANNER_WORKER_PID=$!
echo "        PID: $PLANNER_WORKER_PID"

echo "[6/6] Starting Planner Validator..."
"$SCRIPT_DIR/launch-planner-validator.sh" > "$SCRIPT_DIR/logs/launcher/planner-validator.log" 2>&1 &
PLANNER_VALIDATOR_PID=$!
echo "        PID: $PLANNER_VALIDATOR_PID"

echo ""
echo "================================"
echo "All agents launched!"
echo "================================"
echo ""
echo "PIDs:"
echo "  Scout Worker:     $SCOUT_WORKER_PID"
echo "  Scout Validator:  $SCOUT_VALIDATOR_PID"
echo "  Analyst Worker:   $ANALYST_WORKER_PID"
echo "  Analyst Validator: $ANALYST_VALIDATOR_PID"
echo "  Planner Worker:   $PLANNER_WORKER_PID"
echo "  Planner Validator: $PLANNER_VALIDATOR_PID"
echo ""
echo "Logs: $SCRIPT_DIR/logs/launcher/"
echo ""
echo "To stop all agents:"
echo "  kill $SCOUT_WORKER_PID $SCOUT_VALIDATOR_PID $ANALYST_WORKER_PID $ANALYST_VALIDATOR_PID $PLANNER_WORKER_PID $PLANNER_VALIDATOR_PID"
echo ""
echo "To check status:"
echo "  cat $SCRIPT_DIR/communications/heartbeat.yaml"
echo ""

# Save PIDs to file
cat > "$SCRIPT_DIR/.pids" << EOF
SCOUT_WORKER_PID=$SCOUT_WORKER_PID
SCOUT_VALIDATOR_PID=$SCOUT_VALIDATOR_PID
ANALYST_WORKER_PID=$ANALYST_WORKER_PID
ANALYST_VALIDATOR_PID=$ANALYST_VALIDATOR_PID
PLANNER_WORKER_PID=$PLANNER_WORKER_PID
PLANNER_VALIDATOR_PID=$PLANNER_VALIDATOR_PID
EOF

echo "PIDs saved to: $SCRIPT_DIR/.pids"
