#!/bin/bash
# Moltbot MCP Connection Script
# Sets up MCP connection from MacBook to Moltbot on VPS

set -e

VPS_IP="77.42.66.40"
MCP_CONFIG="~/.blackbox5/.mcp-moltbot.json"

echo "═══════════════════════════════════════════════════════════════"
echo "  Moltbot MCP Connection Setup"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "→ Testing MCP connections..."

# Test ralf-vps (SSH)
if ssh -i ~/.ssh/ralf_hetzner root@77.42.66.40 "ls /opt/ralf/mcp-server.py" > /dev/null 2>&1; then
    echo "✓ ralf-vps MCP server accessible"
else
    echo "✗ ralf-vps MCP server not found"
fi

# Test moltbot-vps (local stdio)
if echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize"}' | python3 ~/.blackbox5/mcp-server-moltbot.py > /dev/null 2>&1; then
    echo "✓ moltbot-vps MCP server working"
else
    echo "✗ moltbot-vps MCP server error"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  MCP Setup Complete"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "To start Claude Code with MCP:"
echo "  cd ~/.blackbox5 && claude --mcp-config .mcp-moltbot.json"
echo ""
echo "Available MCP tools:"
echo ""
echo "  ralf-vps (via SSH):"
echo "    • ralf_get_queue       - Get RALF task queue"
echo "    • ralf_get_events      - Get RALF events"
echo "    • ralf_list_tasks      - List all tasks"
echo "    • ralf_get_task_status - Get specific task status"
echo "    • ralf_run_command     - Run command on RALF VPS"
echo ""
echo "  moltbot-vps (local stdio):"
echo "    • moltbot_get_status       - Check OpenClaw gateway"
echo "    • moltbot_send_message     - Send Telegram message"
echo "    • moltbot_get_ralf_status  - Get RALF queue via Moltbot"
echo "    • moltbot_get_user_context - Get user profile"
echo "    • moltbot_run_command      - Run command on VPS"
echo ""
echo "MCP Config: ${MCP_CONFIG}"
echo ""
