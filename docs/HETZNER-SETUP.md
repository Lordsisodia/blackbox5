# RALF Hetzner Setup Guide

Complete guide to running RALF agents on Hetzner Cloud VPS.

## Option 1: Automated Setup (Recommended)

### Prerequisites
1. Hetzner Cloud account: https://hetzner.com/cloud
2. Hetzner API token from: https://console.hetzner.cloud/projects
3. hcloud CLI installed:
   ```bash
   brew install hcloud  # macOS
   # OR download from https://github.com/hetznercloud/cli/releases
   ```

### Run Automated Setup

```bash
# Set your API token
export HETZNER_API_TOKEN=your_token_here

# Run setup script
bin/setup-hetzner-ralf
```

This will:
- Create CX23 server (4GB RAM, ~$4/month)
- Install Docker and dependencies
- Setup GitHub Actions deployment
- Print connection info

## Option 2: Manual Setup

### Step 1: Create Server
1. Go to https://console.hetzner.cloud/projects
2. Click "Add Server"
3. Choose:
   - **Type:** CX23 (4GB RAM, 2 vCPUs) - $4.51/month
   - **Image:** Ubuntu 22.04
   - **Location:** Nuremberg (nbg1) or Falkenstein (fsn1)
   - **SSH Key:** Add your public key
4. Click "Create & Buy"

### Step 2: Connect to Server
```bash
ssh root@your-server-ip
```

### Step 3: Install Docker
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### Step 4: Clone Repository
```bash
cd /opt
git clone https://github.com/Lordsisodia/blackbox5.git ralf
cd ralf
```

### Step 5: Create Environment File
```bash
cat > .env << EOF
ANTHROPIC_API_KEY=your_glm_key_here
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
RALF_PROJECT_DIR=/opt/ralf/5-project-memory/blackbox5
RALF_ENGINE_DIR=/opt/ralf/2-engine/.autonomous
EOF
```

### Step 6: Create Docker Compose
```bash
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
        apt-get update &&
        apt-get install -y curl git tmux python3 python3-pip netcat-openbsd &&
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
        apt-get update &&
        apt-get install -y curl git tmux python3 python3-pip netcat-openbsd &&
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
        pip install flask &&
        echo 'from flask import Flask; import datetime; app = Flask(__name__); app.route(\"/\")(lambda: f\"RALF OK - {datetime.datetime.utcnow().isoformat()}\"); app.run(host=\"0.0.0.0\", port=8080)' > server.py &&
        python server.py
      "
    restart: unless-stopped
    mem_limit: 256m
EOF
```

### Step 7: Start Agents
```bash
docker compose up -d
```

### Step 8: View Logs
```bash
# View planner logs
docker logs -f ralf-planner

# View executor logs
docker logs -f ralf-executor

# View both
docker logs -f ralf-planner &
docker logs -f ralf-executor &
```

## Connecting to the Server

### Quick Connect
```bash
# Using the SSH key generated during setup
ssh -i ~/.ssh/ralf_hetzner root@77.42.66.40
```

### Server Details
- **IP Address:** 77.42.66.40
- **Location:** Helsinki (hel1)
- **Type:** CX23 (4GB RAM, 2 vCPUs)
- **OS:** Ubuntu 22.04
- **User:** root (primary), ralf (agent user)

### Repository Location on Server
```bash
# Main repository
/opt/ralf

# Blackbox5 code
/opt/ralf/5-project-memory/blackbox5

# Agent runs (planner)
/opt/ralf/5-project-memory/blackbox5/runs/planner/

# Agent runs (executor)
/opt/ralf/5-project-memory/blackbox5/runs/executor/
```

### Checking Agent Status
```bash
# View tmux sessions (agents run in tmux)
tmux ls

# Attach to planner session
tmux attach -t ralf-planner

# Attach to executor session
tmux attach -t ralf-executor

# View logs
tail -f /tmp/planner.log
tail -f /tmp/executor.log
```

### GitHub Authentication
The server is configured with SSH key for GitHub:
```bash
# Test GitHub connection
ssh -T git@github.com

# Git config is set for ralf user
su - ralf
cd /opt/ralf
git status
```

## Connecting to Agents (Docker - Legacy)

### SSH Directly
```bash
ssh root@your-server-ip
docker ps                    # See running containers
docker logs ralf-planner     # View planner logs
docker logs ralf-executor    # View executor logs
```

### From Your Laptop
```bash
# View logs without SSHing in
ssh root@your-server-ip 'docker logs ralf-planner'
ssh root@your-server-ip 'docker logs ralf-executor'

# Check status
ssh root@your-server-ip 'docker ps'

# Restart agents
ssh root@your-server-ip 'docker compose restart'
```

## GitHub Actions Auto-Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Hetzner

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Hetzner
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HETZNER_IP }}
          username: root
          key: ${{ secrets.HETZNER_SSH_KEY }}
          script: |
            cd /opt/ralf
            git pull origin main
            docker compose up -d
```

Add these secrets to GitHub (Settings → Secrets → Actions):
- `HETZNER_IP`: Your server IP address
- `HETZNER_SSH_KEY`: Content of your private SSH key

## Monitoring

### Install Portainer (Web UI)
```bash
docker run -d -p 8000:8000 -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce:latest
```

Access at: `https://your-server-ip:9443`

### Resource Usage
```bash
# Check CPU/RAM usage
htop

# Check disk usage
df -h

# Check Docker stats
docker stats
```

## Troubleshooting

### Agents Not Starting
```bash
# Check logs
docker logs ralf-planner
docker logs ralf-executor

# Restart
docker compose restart
```

### Out of Memory
```bash
# Check memory
docker stats

# Add swap if needed
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

### Claude Not Found
```bash
# Install manually
curl -fsSL https://claude.ai/install | sh
```

## Costs

- **Hetzner CX23**: €4.51/month (~$4.90/month)
- **Data transfer**: 20TB included
- **No hidden fees**

## Security

- Firewall enabled by default on Hetzner
- SSH key authentication only
- Keep your SSH key secure
- Consider UFW for additional firewall rules:
  ```bash
  ufw allow 22/tcp
  ufw allow 8080/tcp
  ufw enable
  ```
