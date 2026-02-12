# SUBTASK-004E: VPS Deployment Package

**Parent Task:** TASK-AUTONOMY-004
**Depends On:** SUBTASK-004B, SUBTASK-004C, SUBTASK-004D
**Status:** pending
**Priority:** HIGH
**Estimated Tokens:** 25K

---

## Objective

Create complete deployment package for VPS including systemd service, logrotate config, environment setup, and documentation.

---

## Success Criteria

- [ ] Systemd service auto-starts on boot
- [ ] Logrotate manages log files
- [ ] Environment setup script works
- [ ] Telegram bot setup documented
- [ ] Deployment documentation complete
- [ ] Health check endpoint works

---

## Implementation Plan

### Step 1: Systemd Service File (4K tokens)
Create `/etc/systemd/system/bb5-watch.service`:

```ini
[Unit]
Description=BB5 Health Monitor Daemon
Documentation=https://github.com/shaansisodia/blackbox5/docs/health-monitoring
After=network.target

[Service]
Type=simple
User=%I
Group=%I
WorkingDirectory=/home/%I/.blackbox5
Environment=PYTHONPATH=/home/%I/.blackbox5/bin/lib
Environment=BB5_HOME=/home/%I/.blackbox5
EnvironmentFile=/home/%I/.blackbox5/config/watch.env
ExecStart=/home/%I/.blackbox5/bin/bb5-watch start --foreground
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10s
StartLimitInterval=60s
StartLimitBurst=3

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=false
ReadWritePaths=/home/%I/.blackbox5/.autonomous/health

[Install]
WantedBy=multi-user.target
```

Enable with: `systemctl enable bb5-watch@shaansisodia`

### Step 2: Logrotate Configuration (3K tokens)
Create `/etc/logrotate.d/bb5-health`:

```
/home/*/.blackbox5/.autonomous/health/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0644 %USER% %USER%
    size 100M

    postrotate
        /bin/systemctl reload bb5-watch@* > /dev/null 2>&1 || true
    endscript
}
```

### Step 3: Environment Setup Script (5K tokens)
Create `~/.blackbox5/bin/setup-health-monitoring.sh`:

```bash
#!/bin/bash
# Setup script for BB5 health monitoring

set -e

echo "Setting up BB5 Health Monitoring..."

# Create directories
mkdir -p ~/.blackbox5/.autonomous/health
mkdir -p ~/.blackbox5/config
mkdir -p ~/.blackbox5/bin/lib/health_monitor

# Check Python version
python3 --version

# Install dependencies
pip3 install --user pyyaml rich click python-telegram-bot

# Create config from template
if [ ! -f ~/.blackbox5/config/watch-config.yaml ]; then
    cp ~/.blackbox5/config/watch-config.example.yaml ~/.blackbox5/config/watch-config.yaml
    echo "Created config file. Please edit ~/.blackbox5/config/watch-config.yaml"
fi

# Create environment file
if [ ! -f ~/.blackbox5/config/watch.env ]; then
    cat > ~/.blackbox5/config/watch.env << 'EOF'
# BB5 Watch Environment
# Get token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EOF
    echo "Created env file. Please edit ~/.blackbox5/config/watch.env"
fi

# Set permissions
chmod 600 ~/.blackbox5/config/watch.env
chmod 644 ~/.blackbox5/config/watch-config.yaml

# Initialize database
python3 -c "from health_monitor.database import init_database; init_database()"

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit ~/.blackbox5/config/watch.env with your Telegram credentials"
echo "2. Edit ~/.blackbox5/config/watch-config.yaml with your preferences"
echo "3. Test: bb5-health"
echo "4. Start daemon: bb5-watch start"
echo "5. Enable auto-start: sudo systemctl enable bb5-watch@$USER"
```

### Step 4: Telegram Bot Setup Guide (4K tokens)
Create `~/.blackbox5/docs/TELEGRAM_SETUP.md`:

```markdown
# Telegram Bot Setup for BB5 Alerts

## 1. Create Bot

1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose name (e.g., "BB5 Monitor")
4. Choose username (e.g., "bb5_monitor_bot")
5. Save the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 2. Get Chat ID

### Option A: Personal Messages
1. Message your new bot
2. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Look for `"chat":{"id":12345678`
4. The ID is `12345678`

### Option B: Group Chat
1. Add bot to group
2. Send a message in group
3. Visit API URL above
4. Look for negative ID (e.g., `-12345678`)

## 3. Configure

Edit `~/.blackbox5/config/watch.env`:

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=12345678
```

## 4. Test

```bash
bb5-watch test-alert telegram
```

You should receive a test message.
```

### Step 5: Deployment Documentation (5K tokens)
Create `~/.blackbox5/docs/VPS_DEPLOYMENT.md`:

```markdown
# BB5 Health Monitoring - VPS Deployment Guide

## Prerequisites

- Ubuntu 20.04+ or Debian 11+
- Python 3.9+
- Systemd
- 512MB RAM minimum (1GB recommended)

## Quick Start

```bash
# 1. Clone/setup BB5 (if not done)
cd ~
git clone <your-repo> .blackbox5

# 2. Run setup
~/.blackbox5/bin/setup-health-monitoring.sh

# 3. Configure Telegram
nano ~/.blackbox5/config/watch.env

# 4. Test
bb5-health

# 5. Install systemd service
sudo cp ~/.blackbox5/config/systemd/bb5-watch.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bb5-watch@$USER
sudo systemctl start bb5-watch@$USER

# 6. Check status
sudo systemctl status bb5-watch@$USER
bb5-watch status
```

## Monitoring

### View Logs

```bash
# Live logs
journalctl -u bb5-watch@$USER -f

# Log files
tail -f ~/.blackbox5/.autonomous/health/watch.log
```

### Health Check

```bash
# Quick check
bb5-health

# JSON for external monitoring
curl -s http://localhost:8080/health | jq .
```

## Troubleshooting

### Daemon won't start

```bash
# Check logs
journalctl -u bb5-watch@$USER --since "1 hour ago"

# Test in foreground
bb5-watch start --foreground
```

### No Telegram alerts

1. Check token: `cat ~/.blackbox5/config/watch.env`
2. Test manually: `bb5-watch test-alert telegram`
3. Check logs for errors

### High memory usage

- Reduce check frequency in config
- Lower history retention
- Enable SQLite WAL mode

## Security

- Config files are chmod 600 (user readable only)
- No secrets in logs
- Telegram tokens in env file, not config
- Systemd sandboxing enabled

## Uninstall

```bash
sudo systemctl stop bb5-watch@$USER
sudo systemctl disable bb5-watch@$USER
sudo rm /etc/systemd/system/bb5-watch.service
sudo rm /etc/logrotate.d/bb5-health
```
```

### Step 6: Health Check Endpoint (4K tokens)
Optional HTTP endpoint for external monitoring:

```python
# Add to daemon.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health_endpoint():
    """HTTP health check endpoint"""
    data = collect_all()
    score = calculate_health_score(data)

    return jsonify({
        'status': 'healthy' if score >= 60 else 'unhealthy',
        'health_score': score,
        'timestamp': datetime.now().isoformat(),
        'queue': {
            'pending': data['queue']['pending'],
            'in_progress': data['queue']['in_progress']
        },
        'agents': {
            'total': len(data['agents']),
            'online': sum(1 for a in data['agents'] if a.is_online())
        }
    })

# Run on port 8080 (configurable)
```

---

## Files to Create

1. `/etc/systemd/system/bb5-watch.service`
2. `/etc/logrotate.d/bb5-health`
3. `~/.blackbox5/bin/setup-health-monitoring.sh`
4. `~/.blackbox5/config/watch-config.example.yaml`
5. `~/.blackbox5/docs/TELEGRAM_SETUP.md`
6. `~/.blackbox5/docs/VPS_DEPLOYMENT.md`

---

## Testing

```bash
# Test setup script
./setup-health-monitoring.sh

# Test systemd (local)
systemctl --user enable ~/.blackbox5/config/systemd/bb5-watch.service
systemctl --user start bb5-watch

# Test logrotate
logrotate -d /etc/logrotate.d/bb5-health
```

---

## Definition of Done

- [ ] Systemd service works
- [ ] Logrotate works
- [ ] Setup script runs without errors
- [ ] Telegram setup guide is clear
- [ ] Deployment docs are complete
- [ ] Health endpoint responds (if implemented)
- [ ] Clean uninstall process documented
