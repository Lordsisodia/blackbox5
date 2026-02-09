#!/bin/bash
# Deploy MoltBot with per-run Telegram updates to VPS

set -e

VPS_HOST="${VPS_HOST:-root@77.42.66.40}"
BB5_DIR="/opt/blackbox5"

echo "Deploying MoltBot with per-run Telegram updates..."
echo "VPS: $VPS_HOST"
echo ""

# Check if we can connect
echo "Checking VPS connection..."
if ! ssh -o ConnectTimeout=5 "$VPS_HOST" "echo 'Connected'" 2>/dev/null; then
    echo "ERROR: Cannot connect to VPS at $VPS_HOST"
    echo "Make sure you have SSH access configured"
    exit 1
fi

echo "✓ VPS connection OK"
echo ""

# Copy updated files
echo "Copying updated moltbot-ralf-manager.sh..."
scp moltbot-ralf-manager.sh "$VPS_HOST:$BB5_DIR/agents/moltbot-autonomous/"

echo "Copying updated moltbot-agent.py (v2 with metrics)..."
scp moltbot-agent.py "$VPS_HOST:$BB5_DIR/agents/moltbot-autonomous/"

echo "✓ Files copied"
echo ""

# Restart the service
echo "Restarting blackbox5-agent service..."
ssh "$VPS_HOST" "systemctl restart blackbox5-agent"

echo "Checking service status..."
ssh "$VPS_HOST" "systemctl status blackbox5-agent --no-pager -l"

echo ""
echo "═══════════════════════════════════════════════════"
echo "Deployment Complete!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "MoltBot will now:"
echo "  1. Send a startup notification to Telegram"
echo "  2. Send an update after EVERY run completes"
echo ""
echo "Each update includes:"
echo "  • Run ID and status (✅/❌/⚠️)"
echo "  • Action that was executed"
echo "  • Duration of the run"
echo "  • Git commits/pushes"
echo "  • Result summary"
echo ""
echo "To view logs:"
echo "  ssh $VPS_HOST 'journalctl -u blackbox5-agent -f'"
echo ""
echo "To configure Telegram topic ID:"
echo "  Edit $BB5_DIR/agents/moltbot-autonomous/moltbot-ralf-manager.sh"
echo "  Set TELEGRAM_TOPIC_ID to your Blackbox topic ID"
echo ""
