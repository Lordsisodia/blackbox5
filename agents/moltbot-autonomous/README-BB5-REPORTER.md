# BB5 Agent Activity Reporter

A Telegram bot that periodically reports what BB5 agents have accomplished.

## Overview

This reporter runs alongside MoltBot on your VPS and sends periodic updates to the Telegram channel about:

- Agent activity (which agents ran, what they did)
- Tasks completed, started, and in progress
- Discoveries made by agents
- Errors or issues encountered
- Daily summaries of all activity

## Files

| File | Purpose |
|------|---------|
| `bb5-reporter.py` | Main reporter agent (Python) |
| `bb5-reporter.service` | systemd service definition |
| `setup-reporter.sh` | One-command setup script |
| `send-update.sh` | Manual update trigger |

## Installation on VPS

```bash
# SSH to your VPS
ssh root@77.42.66.40

# Navigate to the agent directory
cd /opt/blackbox5/agents/moltbot-autonomous

# Run the setup script
sudo ./setup-reporter.sh

# Start the service
sudo systemctl start bb5-reporter

# Check it's running
sudo systemctl status bb5-reporter
```

## Telegram Commands

Once running, reply to bot messages with:

| Command | Action |
|---------|--------|
| `status` | Full system status (24h) |
| `tasks` | List current tasks |
| `agents` | Agent activity details |
| `report` | Immediate hourly report |
| `report 6` | Report for last 6 hours |
| `daily` | Daily summary |

## Update Schedule

- **Hourly updates**: Every hour during business hours (9 AM - 9 PM)
- **Daily summary**: Every day at 9 AM
- **Command responses**: Immediate

## How It Works

1. **Reads events**: Parses `events.yaml` from BB5 communications
2. **Analyzes activity**: Categorizes events by type (started, completed, errors, etc.)
3. **Reads filesystem**: Checks active tasks, recent runs
4. **Formats report**: Creates human-friendly Telegram messages
5. **Sends updates**: Posts to the configured Telegram chat/topic

## Configuration

Edit the service file to change:

```bash
# Telegram settings
Environment="TELEGRAM_BOT_TOKEN=8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo"
Environment="TELEGRAM_CHAT_ID=7643203581"

# To use a specific topic (like your Blackbox topic):
# Edit bb5-reporter.py and set self.topic_id = YOUR_TOPIC_ID
```

## Logs

```bash
# View real-time logs
sudo journalctl -u bb5-reporter -f

# View recent logs
sudo journalctl -u bb5-reporter --since "1 hour ago"
```

## Manual Testing

```bash
# Send a test message
cd /opt/blackbox5/agents/moltbot-autonomous
python3 -c "
import requests
requests.post(
    'https://api.telegram.org/bot8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo/sendMessage',
    json={'chat_id': '7643203581', 'text': '📊 Test message from BB5 Reporter'}
)
"

# Send an immediate update
./send-update.sh 1  # Last 1 hour
./send-update.sh 24 # Last 24 hours
```

## Integration with MoltBot

This reporter complements MoltBot:

- **MoltBot**: Analyzes BB5 for issues, proposes fixes, executes actions
- **BB5 Reporter**: Reports what agents have done, tracks activity

Both can run simultaneously on the same VPS.

## Troubleshooting

**No messages received:**
- Check bot token and chat ID are correct
- Verify bot has permission to post in the channel
- Check logs: `sudo journalctl -u bb5-reporter -f`

**Empty reports:**
- Events file may be empty or in different location
- Check: `cat /opt/blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`

**Service won't start:**
- Check Python dependencies: `pip3 install pyyaml schedule requests`
- Check file permissions: `ls -la /opt/blackbox5/agents/moltbot-autonomous/`
