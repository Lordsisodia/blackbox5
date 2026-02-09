#!/bin/bash
# deploy-to-vps.sh - Deploy BlackBox5 infrastructure to VPS
# Usage: ./deploy-to-vps.sh [branch-name]

set -e

VPS_HOST="hellzinger"
VPS_USER="${VPS_USER:-root}"
BB5_DIR="$HOME/.blackbox5"
BRANCH="${1:-autonomous-improvement}"

echo "=== BlackBox5 VPS Deployment ==="
echo "Branch: $BRANCH"
echo "VPS: $VPS_HOST"
echo ""

# Ensure we're on the right branch
cd "$BB5_DIR"
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

# Sync to VPS
echo "Syncing BlackBox5 to VPS..."
rsync -avz --progress \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    "$BB5_DIR/" \
    "$VPS_USER@$VPS_HOST:/opt/blackbox5/"

# SSH into VPS and setup
echo "Setting up on VPS..."
ssh "$VPS_USER@$VPS_HOST" << EOF
    cd /opt/blackbox5

    # Setup .claude directory
    mkdir -p /root/.claude/hooks
    mkdir -p /root/.claude/agents
    mkdir -p /root/.claude/skills

    # Copy hooks
    cp -r .claude/hooks/* /root/.claude/hooks/ 2>/dev/null || true

    # Copy agents
    cp -r .claude/agents/* /root/.claude/agents/ 2>/dev/null || true

    # Copy settings
    cp .claude/settings.json /root/.claude/settings.json 2>/dev/null || true

    # Make hooks executable
    chmod +x /root/.claude/hooks/*.sh

    # Setup project memory
    mkdir -p /opt/blackbox5/5-project-memory/blackbox5/.autonomous

    # Install bb5 CLI
    cp bin/bb5 /usr/local/bin/bb5 2>/dev/null || true
    chmod +x /usr/local/bin/bb5

    echo "Setup complete on VPS"
EOF

echo ""
echo "=== Deployment Complete ==="
echo "Branch '$BRANCH' deployed to $VPS_HOST"
echo ""
echo "To activate autonomous mode on VPS:"
echo "  ssh $VPS_USER@$VPS_HOST"
echo "  cd /opt/blackbox5"
echo "  ./bin/start-autonomous.sh"
