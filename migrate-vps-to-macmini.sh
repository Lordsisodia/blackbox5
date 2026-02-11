#!/bin/bash
# Migrate MoltBot and configurations from VPS to Mac Mini

set -e

echo "=========================================="
echo "VPS to Mac Mini Migration"
echo "=========================================="
echo ""

VPS_IP="77.42.66.40"
VPS_KEY="~/.ssh/ralf_hetzner"
MAC_MINI="mac-mini"
MIGRATION_DIR="~/.vps-migration-$(date +%Y%m%d_%H%M%S)"

echo "Step 1: Creating migration directory on Mac Mini..."
ssh $MAC_MINI "mkdir -p $MIGRATION_DIR"

echo ""
echo "Step 2: Copying MoltBot configuration..."
ssh -i $VPS_KEY root@$VPS_IP "tar czf - /opt/moltbot /root/.openclaw" | ssh $MAC_MINI "tar xzf - -C $MIGRATION_DIR/"

echo ""
echo "Step 3: Copying blackbox5 configs..."
ssh -i $VPS_KEY root@$VPS_IP "tar czf - /opt/blackbox5/.mcp-moltbot.json /opt/blackbox5/mcp-*.py /opt/blackbox5/moltbot*.json" 2>/dev/null | ssh $MAC_MINI "tar xzf - -C $MIGRATION_DIR/ 2>/dev/null || true"

echo ""
echo "Step 4: Copying bridge scripts..."
ssh -i $VPS_KEY root@$VPS_IP "tar czf - /opt/*bridge*.py /opt/NATS_SETUP.md" 2>/dev/null | ssh $MAC_MINI "tar xzf - -C $MIGRATION_DIR/ 2>/dev/null || true"

echo ""
echo "Step 5: Setting up on Mac Mini..."
ssh $MAC_MINI << 'SETUP_SCRIPT'

# Create directories
mkdir -p ~/.openclaw
mkdir -p /opt/moltbot
mkdir -p ~/Projects/moltbot

# Find migration directory
MIGRATION_DIR=$(ls -td ~/.vps-migration-* 2>/dev/null | head -1)

if [ -z "$MIGRATION_DIR" ]; then
    echo "ERROR: No migration directory found"
    exit 1
fi

echo "Using migration directory: $MIGRATION_DIR"

# Copy OpenClaw config
if [ -d "$MIGRATION_DIR/root/.openclaw" ]; then
    cp -r "$MIGRATION_DIR/root/.openclaw"/* ~/.openclaw/
    echo "✓ Copied .openclaw configuration"
fi

# Copy MoltBot
if [ -d "$MIGRATION_DIR/opt/moltbot" ]; then
    sudo cp -r "$MIGRATION_DIR/opt/moltbot"/* /opt/moltbot/ 2>/dev/null || cp -r "$MIGRATION_DIR/opt/moltbot"/* ~/Projects/moltbot/
    echo "✓ Copied MoltBot"
fi

# Set permissions
chmod -R 700 ~/.openclaw/credentials 2>/dev/null || true
chmod -R 700 ~/.openclaw/telegram 2>/dev/null || true

echo ""
echo "Setup complete!"
echo ""

SETUP_SCRIPT

echo ""
echo "=========================================="
echo "Migration Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Install OpenClaw on Mac Mini if not present"
echo "2. Set up LaunchAgent for MoltBot"
echo "3. Test Telegram bot connection"
echo "4. Update MCP configurations"
echo ""
