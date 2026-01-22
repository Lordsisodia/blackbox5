#!/bin/bash
# Test workflow for Task Registry System

set -e

echo "🧪 Testing Task Registry System"
echo "=================================="
echo ""

# Create a temporary registry for testing
export TASK_REGISTRY_PATH="./data/test_registry.json"

# Clean up any existing test registry
rm -f "$TASK_REGISTRY_PATH"

echo "1️⃣  Importing tasks from epic..."
python -m task_registry.cli import-epic \
  ../../../5-project-memory/siso-internal/plans/active/user-profile/epic.md \
  --breakdown ../../../5-project-memory/siso-internal/plans/active/user-profile/TASK-BREAKDOWN.md \
  --objective user-profile

echo ""
echo "2️⃣  Showing statistics..."
python -m task_registry.cli stats

echo ""
echo "3️⃣  Showing available tasks..."
python -m task_registry.cli available

echo ""
echo "4️⃣  Simulating agent workflow..."
echo "   - Taking first available task..."
python -m task_registry.cli take TASK-1-1 --agent test-agent

echo "   - Starting the task..."
python -m task_registry.cli start TASK-1-1

echo "   - Completing the task..."
python -m task_registry.cli complete TASK-1-1

echo ""
echo "5️⃣  Checking what's now available..."
python -m task_registry.cli available

echo ""
echo "6️⃣  Showing task status..."
python -m task_registry.cli status TASK-1-1

echo ""
echo "7️⃣  Checking workspace..."
WORKSPACE=$(python -m task_registry.cli workspace TASK-1-1)
echo "   Workspace: $WORKSPACE"
echo "   Contents:"
ls -la "$WORKSPACE" || echo "   (Workspace not created in this test)"

echo ""
echo "✅ Test workflow complete!"
echo ""
echo "To clean up, run: rm $TASK_REGISTRY_PATH"
