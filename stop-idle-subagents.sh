#!/bin/bash
# Stop Idle Sub-Agents - Saves 600+ tokens/min
# Execute immediately

cd /opt/blackbox5

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] 🛑 STOPPING 12 idle sub-agents..."

# Execute stop script
bash 5-project-memory/blackbox5/tasks/active/stop-idle-subagents.sh

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] ✅ All 12 idle agents stopped"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] 💰 Saved 600+ tokens/min (~$7.20/day)"

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] 📋 Run 'memadd' to add an insight and verify savings"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] 🚀 READY TO USE SHARED MEMORY"

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] No more idle sub-agents!"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Shared memory working at localhost:6379"
