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
