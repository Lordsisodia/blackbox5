# BB5 Health Dashboard - VPS Deployment Guide

This guide covers deploying the BB5 Health Dashboard system on a VPS for 24/7 monitoring.

## Overview

The health monitoring system consists of three components:

1. **bb5-health** - CLI snapshot tool for manual checks
2. **bb5-dashboard** - Live terminal UI dashboard
3. **bb5-watch** - Background daemon with alerting

## Prerequisites

- Python 3.9+
- pip
- systemd (for service management)
- BB5 installation at `~/.blackbox5`

## Installation

### 1. Install Dependencies

```bash
pip install pyyaml rich python-telegram-bot requests
```

### 2. Verify BB5 Health Tools

```bash
# Check tools are executable
ls -la ~/.blackbox5/bin/bb5-*

# Test health command
~/.blackbox5/bin/bb5-health

# Test watch status
~/.blackbox5/bin/bb5-watch status
```

### 3. Configure Telegram Alerts (Optional)

Edit `~/.blackbox5/.autonomous/health/environment`:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
ALERT_MIN_SEVERITY=warning
ALERT_COOLDOWN_SECONDS=300
```

To get a Telegram bot token:
1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Copy the token provided
4. Get your chat ID by messaging @userinfobot

### 4. Install Systemd Service

```bash
# Copy service file (replace 'user' with your username)
sudo cp ~/.blackbox5/.autonomous/health/bb5-watch.service \
        /etc/systemd/system/bb5-watch@.service

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable bb5-watch@$USER

# Start the service
sudo systemctl start bb5-watch@$USER

# Check status
sudo systemctl status bb5-watch@$USER
```

### 5. Configure Log Rotation

Create `/etc/logrotate.d/bb5-watch`:

```
/home/*/.blackbox5/.autonomous/health/watch.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 user user
}
```

## Usage

### Manual Health Checks

```bash
# Full health snapshot
bb5-health

# JSON output for automation
bb5-health -f json

# CSV output for spreadsheets
bb5-health -f csv

# Queue stats only
bb5-health -q

# Agent stats only
bb5-health -a

# Watch mode (refresh every 5 seconds)
bb5-health -w 5

# Save snapshot to database
bb5-health --save
```

### Live Dashboard

```bash
# Start live dashboard (refresh every 5 seconds)
bb5-dashboard

# Custom refresh interval
bb5-dashboard -r 10
```

Controls:
- `q` or `Ctrl+C` - Quit
- `r` - Force refresh
- `1/2/3` - Switch views (overview/queue/agents)

### Daemon Control

```bash
# Start daemon
bb5-watch start

# Start with Telegram alerts
bb5-watch start -t

# Start in background (daemon mode)
bb5-watch start -d

# Custom check interval (60 seconds)
bb5-watch start -i 60

# Stop daemon
bb5-watch stop

# Check status
bb5-watch status

# View logs
bb5-watch logs

# Restart
bb5-watch restart
```

## Monitoring Metrics

The system tracks:

### Queue Metrics
- Pending tasks count
- In-progress tasks count
- Completed tasks count
- Blocked tasks count
- Queue health score (0-100)

### Agent Metrics
- Online agents count
- Stale agents count
- Offline agents count
- Agent health score (0-100)
- Last heartbeat timestamp

### System Metrics
- Overall health score (0-100)
- Throughput (tasks/day)
- Stuck task detection
- Failed task rate

### Health Score Calculation

Weights:
- Throughput: 25%
- Quality: 25%
- Efficiency: 20%
- Reliability: 15%
- Queue Health: 15%

Status thresholds:
- HEALTHY: score >= 60, no critical agents
- WARNING: score < 60 or stale agents
- CRITICAL: offline agents or score < 40

## Alerting

### Telegram Alerts

Sent for:
- Health score drops below threshold (default: 60)
- Agent heartbeat timeout (default: 120s)
- Tasks stuck >2x estimated time

Cooldown period prevents alert spam (default: 5 minutes).

### Webhook Alerts

Configure WEBHOOK_URL to receive JSON payloads:

```json
{
  "severity": "critical",
  "message": "Health score dropped to 45/100",
  "timestamp": "2026-02-08T01:00:00",
  "context": {
    "health_score": 45,
    "queue": {
      "pending": 23,
      "in_progress": 2
    }
  }
}
```

## Troubleshooting

### Daemon Won't Start

```bash
# Check logs
bb5-watch logs

# Check for errors
journalctl -u bb5-watch@$USER -f

# Verify Python dependencies
python3 -c "import yaml, rich, telegram"
```

### No Data Showing

```bash
# Check data sources exist
ls ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/

# Verify queue.yaml format
head ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml
```

### Telegram Alerts Not Working

```bash
# Test Telegram bot
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"

# Check environment variables
cat ~/.blackbox5/.autonomous/health/environment
```

### Database Issues

```bash
# Reset database (warning: deletes history)
rm ~/.blackbox5/.autonomous/health/health.db

# Check database
sqlite3 ~/.blackbox5/.autonomous/health/health.db ".tables"
```

## Database Schema

SQLite database at `~/.blackbox5/.autonomous/health/health.db`:

### snapshots table
- timestamp
- health_score
- status
- queue_pending
- queue_in_progress
- queue_completed
- agents_online
- agents_stale
- agents_total
- stuck_tasks
- details (JSON)

### metrics table
- timestamp
- name
- value
- unit
- tags (JSON)

## Security Considerations

1. **File Permissions**: Ensure environment file is readable only by owner
   ```bash
   chmod 600 ~/.blackbox5/.autonomous/health/environment
   ```

2. **Telegram Tokens**: Never commit tokens to version control

3. **Database**: SQLite database contains no sensitive data by default

4. **Logs**: Health data may contain task titles - review log rotation

## Performance

Resource usage:
- RAM: ~50-100MB
- CPU: Minimal (<1% on idle)
- Disk: ~10MB/day with default 30s interval
- Network: Only for Telegram/webhook alerts

## Uninstallation

```bash
# Stop and disable service
sudo systemctl stop bb5-watch@$USER
sudo systemctl disable bb5-watch@$USER

# Remove service file
sudo rm /etc/systemd/system/bb5-watch@.service

# Remove database and logs
rm -rf ~/.blackbox5/.autonomous/health/

# Remove tools (optional)
rm ~/.blackbox5/bin/bb5-health
rm ~/.blackbox5/bin/bb5-dashboard
rm ~/.blackbox5/bin/bb5-watch
```

## Support

For issues or questions:
1. Check logs: `bb5-watch logs`
2. Verify configuration: `cat ~/.blackbox5/.autonomous/health/environment`
3. Test manually: `bb5-health -f json`
