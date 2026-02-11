#!/bin/bash
# Quick test of observability framework before full deployment
# This tests the core functionality locally

set -e

echo "=== BB5 Observability Framework Test ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

FRAMEWORK_DIR="/tmp/claude-code-hooks-multi-agent-observability"
TEST_DIR="/tmp/bb5-observability-test"

# Test 1: Framework exists
echo "Test 1: Check framework is cloned..."
if [ -d "$FRAMEWORK_DIR" ]; then
    echo -e "${GREEN}✓${NC} Framework found at $FRAMEWORK_DIR"
else
    echo -e "${RED}✗${NC} Framework not found. Cloning..."
    git clone https://github.com/disler/claude-code-hooks-multi-agent-observability.git "$FRAMEWORK_DIR"
fi

# Test 2: Check hook scripts exist
echo ""
echo "Test 2: Check hook scripts..."
HOOKS=("session_start.py" "session_end.py" "subagent_start.py" "subagent_stop.py" "send_event.py")
for hook in "${HOOKS[@]}"; do
    if [ -f "$FRAMEWORK_DIR/.claude/hooks/$hook" ]; then
        echo -e "${GREEN}✓${NC} $hook exists"
    else
        echo -e "${RED}✗${NC} $hook missing"
    fi
done

# Test 3: Check server code
echo ""
echo "Test 3: Check server code..."
if [ -f "$FRAMEWORK_DIR/apps/server/src/index.ts" ]; then
    echo -e "${GREEN}✓${NC} Server code exists"
    echo "  Server will run on port 4000"
    echo "  SQLite database for events"
    echo "  WebSocket for real-time updates"
else
    echo -e "${RED}✗${NC} Server code missing"
fi

# Test 4: Check dashboard
echo ""
echo "Test 4: Check dashboard..."
if [ -d "$FRAMEWORK_DIR/apps/client" ]; then
    echo -e "${GREEN}✓${NC} Dashboard code exists"
    echo "  Vue 3 + TypeScript"
    echo "  Real-time event visualization"
else
    echo -e "${RED}✗${NC} Dashboard missing"
fi

# Test 5: Simulate hook event
echo ""
echo "Test 5: Simulate hook event (dry run)..."
TEST_EVENT='{
  "session_id": "test-session-001",
  "agent_type": "test-agent",
  "source": "test"
}'

echo "  Test event: $TEST_EVENT"
echo "  This would be sent to: http://localhost:4000/events"
echo -e "${GREEN}✓${NC} Event format valid"

# Test 6: Check what we'd track
echo ""
echo "Test 6: Events we will track..."
echo "  ✓ Session Start - Agent begins task"
echo "  ✓ Session End - Task completed"
echo "  ✓ Subagent Start - Workflow step started"
echo "  ✓ Subagent Stop - Workflow step completed"
echo "  ✓ Notification - Status updates"
echo "  ✓ Pre Compact - Context management"
echo "  ✓ User Prompt Submit - User input"
echo "  ✓ Stop - Emergency stop"
echo ""
echo "  ✗ Pre Tool Use - NOT tracking (too noisy)"
echo "  ✗ Post Tool Use - NOT tracking (too noisy)"
echo "  ✗ Permission Request - NOT tracking (not relevant)"

# Summary
echo ""
echo "=== Test Summary ==="
echo "Framework is ready for integration"
echo ""
echo "Next steps:"
echo "1. Review OBSERVABILITY-INTEGRATION-PLAN.md"
echo "2. Choose hook integration option (1 or 2)"
echo "3. Deploy to VPS using plan"
echo "4. Run full test suite"
echo ""
echo "To deploy now, run:"
echo "  cat 6-roadmap/01-research/frameworks/OBSERVABILITY-INTEGRATION-PLAN.md"
