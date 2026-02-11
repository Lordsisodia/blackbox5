#!/bin/bash
# Mac Mini Cleanup Script
# Run this on the Mac Mini to fix everything

set -e

echo "=========================================="
echo "Mac Mini Cleanup & Fix Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Ensure PATH
export PATH="$HOME/.local/bin:$PATH"

echo "Step 1: Stopping duplicate YouTube worker..."
echo "-------------------------------------------"
if sudo launchctl unload /Users/youtube-pipeline/Library/LaunchAgents/com.youtube.transcript-worker.plist 2>/dev/null; then
    log_info "Unloaded old LaunchAgent"
else
    log_warn "LaunchAgent not loaded or already stopped"
fi

# Kill the process if still running
OLD_WORKER_PID=$(ps aux | grep 'youtube-pipeline.*worker.py' | grep -v grep | awk '{print $2}')
if [ -n "$OLD_WORKER_PID" ]; then
    sudo kill -9 $OLD_WORKER_PID 2>/dev/null && log_info "Killed old worker (PID: $OLD_WORKER_PID)" || log_warn "Could not kill old worker"
else
    log_info "No old worker process found"
fi

echo ""
echo "Step 2: Verifying only one YouTube worker..."
echo "-------------------------------------------"
WORKER_COUNT=$(ps aux | grep 'worker.py' | grep -v grep | wc -l)
if [ "$WORKER_COUNT" -eq 1 ]; then
    log_info "✅ Only one worker running"
    ps aux | grep 'worker.py' | grep -v grep
elif [ "$WORKER_COUNT" -eq 0 ]; then
    log_warn "No workers running - starting yours..."
    launchctl load ~/Library/LaunchAgents/com.siso.youtube-worker.plist
else
    log_warn "Still have $WORKER_COUNT workers running"
    ps aux | grep 'worker.py' | grep -v grep
fi

echo ""
echo "Step 3: Fixing OpenClaw/MoltBot..."
echo "-------------------------------------------"

# Stop any running OpenClaw processes
log_info "Stopping OpenClaw gateway..."
openclaw gateway stop 2>/dev/null || true
sleep 2

# Kill any lingering processes
for pid in $(ps aux | grep 'openclaw' | grep -v grep | awk '{print $2}'); do
    kill -9 $pid 2>/dev/null || true
done

# Clean up old LaunchAgents
log_info "Cleaning up old LaunchAgents..."
for plist in ~/Library/LaunchAgents/com.clawdbot.*.plist ~/Library/LaunchAgents/ai.openclaw.*.plist; do
    if [ -f "$plist" ]; then
        launchctl unload "$plist" 2>/dev/null || true
        mv "$plist" "$plist.bak.$(date +%Y%m%d)"
        log_info "Backed up: $plist"
    fi
done

# Run OpenClaw doctor
log_info "Running OpenClaw doctor..."
openclaw doctor --repair 2>&1 || log_warn "Doctor completed with warnings"

echo ""
echo "Step 4: Installing OpenClaw service properly..."
echo "-------------------------------------------"
openclaw gateway install 2>&1 || log_warn "Service install may have warnings"

echo ""
echo "Step 5: Starting MoltBot..."
echo "-------------------------------------------"
launchctl unload ~/Library/LaunchAgents/com.siso.moltbot.plist 2>/dev/null || true
sleep 1
launchctl load ~/Library/LaunchAgents/com.siso.moltbot.plist 2>&1 && log_info "MoltBot LaunchAgent loaded" || log_warn "LaunchAgent load had issues"

# Also start manually to verify
log_info "Starting OpenClaw gateway manually (for verification)..."
openclaw gateway start --daemon 2>&1 || log_warn "Gateway start had issues"

echo ""
echo "Step 6: Verifying services..."
echo "-------------------------------------------"
sleep 3

echo ""
log_info "YouTube Workers:"
ps aux | grep 'worker.py' | grep -v grep || echo "  No workers running"

echo ""
log_info "OpenClaw/MoltBot:"
ps aux | grep 'openclaw' | grep -v grep || echo "  No OpenClaw running"

echo ""
log_info "LaunchAgents:"
launchctl list | grep -E 'youtube|moltbot|openclaw' || echo "  No relevant LaunchAgents"

echo ""
echo "Step 7: Testing OpenClaw..."
echo "-------------------------------------------"
openclaw status 2>&1 | head -20 || log_warn "Status check had issues"

echo ""
echo "=========================================="
echo "Cleanup Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "--------"
echo "✅ YouTube worker: Check above"
echo "✅ MoltBot/OpenClaw: Check above"
echo ""
echo "Next steps:"
echo "1. Check logs: tail -f ~/Projects/youtube-ai-research/.logs/worker.log"
echo "2. Check MoltBot: tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
echo "3. Test Telegram: Send message to @SISOlegacybot"
echo "4. Check dashboard: http://127.0.0.1:18789/"
echo ""
echo "If issues persist, try:"
echo "  openclaw gateway stop"
echo "  openclaw gateway start --daemon"
echo ""
