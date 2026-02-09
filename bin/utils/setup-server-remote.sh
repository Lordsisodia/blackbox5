#!/bin/bash
#
# One-command setup for RALF agents on Hetzner server
# Run this ON THE SERVER after SSHing in
#

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "  RALF Server Quick Setup"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Update system
echo "[1/8] Updating system..."
apt-get update -qq

# Install Docker
echo "[2/8] Installing Docker..."
curl -fsSL https://get.docker.com | sh -s -- --quiet
usermod -aG docker root

# Install other tools
echo "[3/8] Installing tools..."
apt-get install -y -qq git tmux htop curl

# Create directories
echo "[4/8] Creating directories..."
mkdir -p /opt/ralf
mkdir -p /opt/ralf/project
mkdir -p /opt/ralf/.autonomous

# Clone repository
echo "[5/8] Cloning Blackbox5 repository..."
cd /opt/ralf
if [ ! -d ".git" ]; then
    git clone https://github.com/Lordsisodia/blackbox5.git .
fi

# Create environment file
echo "[6/8] Creating environment file..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
ANTHROPIC_API_KEY=your_glm_key_here
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
RALF_PROJECT_DIR=/opt/ralf/5-project-memory/blackbox5
RALF_ENGINE_DIR=/opt/ralf/2-engine/.autonomous
EOF
    echo "⚠️  IMPORTANT: Edit .env file and add your GLM API key"
fi

# Create Docker Compose
echo "[7/8] Creating Docker Compose..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  ralf-planner:
    image: debian:bookworm-slim
    container_name: ralf-planner
    env_file: .env
    environment:
      - RALF_MODE=plan
    volumes:
      - .:/app/blackbox5
      - /root/.claude:/root/.claude
    working_dir: /app/blackbox5
    command: >
      bash -c "
        apt-get update -qq &&
        apt-get install -y -qq curl git tmux python3 netcat-openbsd &&
        curl -fsSL https://claude.ai/install | sh &&
        while true; do
          bin/ralf-planner-v2 2>&1 | tee -a /tmp/planner.log
          sleep 5
        done
      "
    restart: unless-stopped
    mem_limit: 2g

  ralf-executor:
    image: debian:bookworm-slim
    container_name: ralf-executor
    env_file: .env
    environment:
      - RALF_MODE=execute
    volumes:
      - .:/app/blackbox5
      - /root/.claude:/root/.claude
    working_dir: /app/blackbox5
    command: >
      bash -c "
        apt-get update -qq &&
        apt-get install -y -qq curl git tmux python3 netcat-openbsd &&
        curl -fsSL https://claude.ai/install | sh &&
        while true; do
          bin/ralf-executor-v2 2>&1 | tee -a /tmp/executor.log
          sleep 5
        done
      "
    restart: unless-stopped
    mem_limit: 2g

  keepalive:
    image: python:3.11-slim
    container_name: ralf-keepalive
    ports:
      - "8080:8080"
    command: >
      bash -c "
        pip install flask -q &&
        echo 'from flask import Flask; import datetime; app = Flask(__name__); app.route(\"/\")(lambda: f\"RALF OK - {datetime.datetime.utcnow().isoformat()}\"); app.run(host=\"0.0.0.0\", port=8080)' > server.py &&
        python server.py
      "
    restart: unless-stopped
    mem_limit: 256m
EOF

echo "[8/8] Setup complete!"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  NEXT STEPS:"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1. Edit the environment file:"
echo "   nano /opt/ralf/.env"
echo "   Add your GLM API key to ANTHROPIC_API_KEY"
echo ""
echo "2. Start the agents:"
echo "   cd /opt/ralf && docker compose up -d"
echo ""
echo "3. View logs:"
echo "   docker logs -f ralf-planner"
echo "   docker logs -f ralf-executor"
echo ""
echo "4. Check status:"
echo "   docker ps"
echo ""
echo "═══════════════════════════════════════════════════════════════"
