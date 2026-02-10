# BB5 RALF VPS Setup Guide

Complete guide for deploying BB5 RALF (Recursive Autonomous Loop Framework) on a VPS for autonomous task execution.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Server Setup](#2-server-setup-step-by-step)
3. [Configuration](#3-configuration)
4. [Service Installation](#4-service-installation)
5. [Verification](#5-verification)
6. [Maintenance](#6-maintenance)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Prerequisites

### Recommended VPS Specifications

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04/24.04 LTS |
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Storage | 20 GB SSD | 50+ GB SSD |
| Network | Stable internet | Low-latency connection |

### Required Packages

```bash
# Core dependencies
git
curl
wget
python3 (3.8+)
python3-pip
nodejs (18+)
npm
rsync

# Optional but recommended
redis-server        # For status monitoring
logrotate          # For log management
htop               # For system monitoring
```

### User Requirements

- Root or sudo access to the VPS
- SSH key pair for authentication
- GitHub account with access to the BlackBox5 repository
- API key for Claude (Anthropic) or GLM

---

## 2. Server Setup (Step-by-Step)

### Step 1: Create the bb5-runner User

```bash
# SSH into your VPS as root
ssh root@your-vps-ip

# Create the bb5-runner user
useradd -m -s /bin/bash bb5-runner

# Set a password (optional, SSH keys recommended)
passwd bb5-runner

# Add to sudoers for service management (optional)
usermod -aG sudo bb5-runner

# Create required directories
mkdir -p /opt/blackbox5
chown bb5-runner:bb5-runner /opt/blackbox5
```

### Step 2: Set Up SSH Keys

```bash
# As bb5-runner user
su - bb5-runner

# Create SSH directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add your public key
cat >> ~/.ssh/authorized_keys << 'EOF'
# Paste your SSH public key here
ssh-ed25519 AAAAC3NzaC... your-email@example.com
EOF

chmod 600 ~/.ssh/authorized_keys

# Test SSH connection from your local machine
ssh bb5-runner@your-vps-ip
```

### Step 3: Install Dependencies

```bash
# Update system packages
apt update && apt upgrade -y

# Install core dependencies
apt install -y \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    rsync \
    logrotate \
    htop \
    redis-server

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Verify installations
claude --version
git --version
python3 --version
node --version
```

### Step 4: Clone Repository

```bash
# As bb5-runner user
su - bb5-runner

# Clone the repository
cd /opt/blackbox5
git clone https://github.com/shaansisodia/blackbox5.git .

# Or if using a specific branch
git clone -b autonomous-improvement https://github.com/shaansisodia/blackbox5.git .

# Configure git
git config user.email "vps@blackbox5.local"
git config user.name "BB5 VPS Runner"
```

### Step 5: Set Up Git Branch (vps)

```bash
cd /opt/blackbox5

# Fetch all branches
git fetch origin

# Create and checkout the vps branch
git checkout -b vps origin/autonomous-improvement 2>/dev/null || git checkout vps

# Set upstream tracking
git branch --set-upstream-to=origin/autonomous-improvement vps 2>/dev/null || true

# Verify branch
git branch -a
```

---

## 3. Configuration

### Step 1: Environment Variables

Create the environment configuration file:

```bash
# As bb5-runner user
su - bb5-runner

# Create environment file
cat > /opt/blackbox5/.env << 'EOF'
# BB5 Configuration
BB5_DIR=/opt/blackbox5
BB5_MODE=autonomous

# AI Provider Configuration
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_BASE_URL=https://api.anthropic.com/v1
CLAUDE_MODEL=claude-sonnet-4-6

# Optional: For GLM fallback/alternative
# GLM_API_KEY=your-glm-api-key-here

# Experimental Features
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Paths
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOME=/home/bb5-runner
EOF

chmod 600 /opt/blackbox5/.env
```

### Step 2: Claude Settings

```bash
# Create .claude directory structure
mkdir -p /home/bb5-runner/.claude/hooks
mkdir -p /home/bb5-runner/.claude/agents
mkdir -p /home/bb5-runner/.claude/skills

# Copy project .claude configuration
cp -r /opt/blackbox5/.claude/* /home/bb5-runner/.claude/ 2>/dev/null || true

# Create settings.json
cat > /home/bb5-runner/.claude/settings.json << 'EOF'
{
  "permissions": {
    "allow_all": true
  },
  "experimental": {
    "agent_teams": true
  }
}
EOF

chown -R bb5-runner:bb5-runner /home/bb5-runner/.claude
```

### Step 3: Service Configuration

The systemd service file is located at:
`/opt/blackbox5/bin/ralf-executor/bb5-ralf-executor.service`

Review and customize if needed:

```ini
[Unit]
Description=BB5 RALF Executor - Unified Task Execution Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/blackbox5
Environment="BB5_DIR=/opt/blackbox5"
Environment="ANTHROPIC_API_KEY=your-key-here"
Environment="ANTHROPIC_BASE_URL=https://api.anthropic.com/v1"
Environment="CLAUDE_MODEL=claude-sonnet-4-6"
Environment="CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1"
Environment="BB5_MODE=autonomous"
ExecStart=/opt/blackbox5/bin/ralf-executor/ralf-wrapper.sh
Restart=always
RestartSec=30
StandardOutput=append:/var/log/bb5-ralf-executor.log
StandardError=append:/var/log/bb5-ralf-executor.log

[Install]
WantedBy=multi-user.target
```

### Step 4: File Permissions

```bash
# As root
chown -R bb5-runner:bb5-runner /opt/blackbox5

# Make scripts executable
chmod +x /opt/blackbox5/bin/ralf-executor/*.sh
chmod +x /opt/blackbox5/bin/*.sh 2>/dev/null || true

# Create log directory
mkdir -p /var/log
chmod 755 /var/log

# Create BB5 log directory
mkdir -p /opt/blackbox5/.autonomous/logs
chown -R bb5-runner:bb5-runner /opt/blackbox5/.autonomous
```

---

## 4. Service Installation

### Step 1: Install systemd Service

```bash
# As root
cp /opt/blackbox5/bin/ralf-executor/bb5-ralf-executor.service \
   /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable service to start on boot
systemctl enable bb5-ralf-executor.service
```

### Step 2: Configure ralf-wrapper.sh

The wrapper script is already configured but verify it exists:

```bash
cat /opt/blackbox5/bin/ralf-executor/ralf-wrapper.sh
```

Expected content:
```bash
#!/bin/bash
# RALF Wrapper: Properly drops privileges to run ralf-core.sh
set -e

# Run the actual ralf-core.sh as bb5-runner using su
# -l (login) ensures proper environment including HOME directory
exec su -l bb5-runner -c 'cd /opt/blackbox5 && BB5_DIR=/opt/blackbox5 BB5_MODE=autonomous /opt/blackbox5/bin/ralf-executor/ralf-core.sh'
```

### Step 3: Set Up Log Rotation

```bash
# Create logrotate configuration
cat > /etc/logrotate.d/bb5-ralf << 'EOF'
/var/log/bb5-ralf-executor.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
    postrotate
        systemctl reload bb5-ralf-executor 2>/dev/null || true
    endscript
}

/opt/blackbox5/.autonomous/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 644 bb5-runner bb5-runner
}
EOF
```

### Step 4: Start the Service

```bash
# Start the service
systemctl start bb5-ralf-executor.service

# Check status
systemctl status bb5-ralf-executor.service
```

---

## 5. Verification

### Check Service Status

```bash
# Check if service is running
systemctl status bb5-ralf-executor.service

# Check process
ps aux | grep ralf

# Check if Claude is running
ps aux | grep claude
```

### View Logs

```bash
# View service logs
tail -f /var/log/bb5-ralf-executor.log

# View RALF core logs
tail -f /opt/blackbox5/.autonomous/logs/ralf-core.log

# View systemd logs
journalctl -u bb5-ralf-executor -f

# View recent runs
ls -la /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/
```

### Run Status Check Script

```bash
# Run the status reporter
/opt/blackbox5/bin/ralf-executor/ralf-status.sh
```

Expected output:
```
=== RALF Autonomous Loop Status ===
Timestamp: Mon Feb 10 10:00:00 UTC 2026

RALF-Core: RUNNING
   PID: 12345
   Uptime: 01:23:45
Claude Code: RUNNING
   PID: 12346
   Running: 00:05:30

=== Current Task ===
Task: TASK-2026-02-10-001
Run Folder: /opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/run-20260210_100000-TASK-2026-02-10-001
Status: IN_PROGRESS
...
```

### Test Manual Execution

```bash
# As bb5-runner user
su - bb5-runner
cd /opt/blackbox5

# Test Claude Code is working
echo "Hello, are you working?" | claude -p --dangerously-skip-permissions

# Test RALF core (dry run)
BB5_MODE=autonomous /opt/blackbox5/bin/ralf-executor/ralf-core.sh --dry-run
```

---

## 6. Maintenance

### Updating the Code

```bash
# As bb5-runner user
su - bb5-runner
cd /opt/blackbox5

# Pull latest changes
git pull origin vps

# Or fetch and merge
git fetch origin
git merge origin/autonomous-improvement
```

### Restarting the Service

```bash
# Restart the service
systemctl restart bb5-ralf-executor.service

# Or reload configuration
systemctl reload bb5-ralf-executor.service

# Stop the service
systemctl stop bb5-ralf-executor.service
```

### Monitoring

```bash
# Set up Redis monitoring (optional)
# Edit /opt/blackbox5/bin/ralf-executor/ralf-redis-reporter.sh
# Then run:
redis-server --daemonize yes
/opt/blackbox5/bin/ralf-executor/ralf-redis-reporter.sh &

# Check Redis status
redis-cli GET ralf:status

# Monitor system resources
htop

# Check disk usage
df -h

# Check memory usage
free -h
```

### Log Management

```bash
# Force log rotation
logrotate -f /etc/logrotate.d/bb5-ralf

# Clear old logs
> /var/log/bb5-ralf-executor.log

# Archive logs
tar -czf ~/bb5-logs-$(date +%Y%m%d).tar.gz /var/log/bb5-ralf-executor.log /opt/blackbox5/.autonomous/logs/
```

---

## 7. Troubleshooting

### Service Won't Start

```bash
# Check for errors
journalctl -u bb5-ralf-executor -n 50

# Check permissions
ls -la /opt/blackbox5/bin/ralf-executor/

# Test wrapper manually
/opt/blackbox5/bin/ralf-executor/ralf-wrapper.sh
```

### Claude Code Not Found

```bash
# Check if claude is installed
which claude
claude --version

# If not found, reinstall
npm install -g @anthropic-ai/claude-code

# Check PATH
echo $PATH
```

### Permission Denied Errors

```bash
# Fix ownership
chown -R bb5-runner:bb5-runner /opt/blackbox5

# Fix script permissions
chmod +x /opt/blackbox5/bin/ralf-executor/*.sh

# Check .claude directory
ls -la /home/bb5-runner/.claude/
```

### API Key Issues

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Test API access
curl -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.anthropic.com/v1/models
```

### Git Issues

```bash
# Check git status
cd /opt/blackbox5
git status

# Fix diverged branches
git fetch origin
git reset --hard origin/vps

# Configure git properly
git config --global user.email "vps@blackbox5.local"
git config --global user.name "BB5 VPS Runner"
```

### Common Error Messages

| Error | Solution |
|-------|----------|
| `No AI provider found` | Install Claude Code: `npm install -g @anthropic-ai/claude-code` |
| `Permission denied` | Check file ownership: `chown -R bb5-runner:bb5-runner /opt/blackbox5` |
| `Failed to pull` | Check network connectivity and git credentials |
| `Task failed after 3 attempts` | Check API key and rate limits |
| `No pending tasks found` | Create tasks in `tasks/active/` directory |

---

## Quick Reference

### Essential Commands

```bash
# Start service
systemctl start bb5-ralf-executor

# Stop service
systemctl stop bb5-ralf-executor

# View logs
tail -f /var/log/bb5-ralf-executor.log

# Check status
systemctl status bb5-ralf-executor
/opt/blackbox5/bin/ralf-executor/ralf-status.sh

# Update code
cd /opt/blackbox5 && git pull origin vps

# Restart after update
systemctl restart bb5-ralf-executor
```

### File Locations

| File/Directory | Path |
|----------------|------|
| Service file | `/etc/systemd/system/bb5-ralf-executor.service` |
| Wrapper script | `/opt/blackbox5/bin/ralf-executor/ralf-wrapper.sh` |
| Core script | `/opt/blackbox5/bin/ralf-executor/ralf-core.sh` |
| Service logs | `/var/log/bb5-ralf-executor.log` |
| RALF logs | `/opt/blackbox5/.autonomous/logs/ralf-core.log` |
| Task directory | `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/tasks/active/` |
| Run directory | `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/` |
| Claude config | `/home/bb5-runner/.claude/settings.json` |

---

## Support

For issues or questions:
1. Check the logs: `/var/log/bb5-ralf-executor.log`
2. Review run outputs: `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/runs/`
3. Consult the BB5 documentation in `/opt/blackbox5/1-docs/`
4. Check the RALF Executor README: `/opt/blackbox5/bin/ralf-executor/README.md`

---

*Last updated: 2026-02-10*
