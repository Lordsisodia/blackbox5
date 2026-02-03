# Telegram Bot Integration

## Bot Details

- **Username:** @SISOlegacybot
- **User ID:** 7643203581 (Shaan's approved ID)
- **Platform:** Telegram
- **Framework:** OpenClaw

## Commands

### RALF Commands

| Command | Description |
|---------|-------------|
| `!ralf status` | Full RALF status report |
| `!ralf queue` | Queue status summary |
| `!ralf task TASK-XXX` | Get specific task details |
| `!ralf health` | System health information |
| `!ralf help` | Show available commands |

### Command Handlers

Implemented in `/opt/moltbot/skills/ralf-status.js`:

```javascript
const commands = {
  'ralf status': async (message) => {
    const report = await skill.handleStatusCommand();
    message.reply(report);
  },

  'ralf queue': async (message) => {
    const report = await skill.handleQueueCommand();
    message.reply(report);
  },

  'ralf task': async (message, args) => {
    const report = await skill.handleTaskCommand(args[0]);
    message.reply(report);
  }
};
```

## Message Format

### Status Report Example

```
🤖 **RALF Status Report**

📋 **Queue**
  • Pending: 3
  • In Progress: 1
  • Claimed: 0
  • Completed: 12
  • Total: 16

📊 **Recent Events**
  ✅ TASK-012 - completed
  🚀 TASK-013 - started
  📝 TASK-011 - updated

🔍 **Verifications**
  • Auto-committed: 8
  • Queued for review: 2
  • Human review: 1

📝 **Git Status**
```
94d04b8 ralf: [run-20260204-034800] [unknown] - run completion
```

💻 **System**
  • Uptime: up 3 days, 2 hours
  • Disk: 45%
```

## Security

### User Authentication

Only approved Telegram user IDs can interact with the bot:

```json
{
  "user": {
    "telegram_id": "7643203581"
  }
}
```

### Pairing Process

1. User starts chat with @SISOlegacybot
2. Bot checks if user ID is in whitelist
3. If approved, commands are processed
4. If not approved, message is ignored

## Notification Flow

### Automatic Notifications

1. RALF watcher script runs every 2 minutes (cron)
2. Checks if events.yaml has been modified
3. If new events detected, sends notification
4. Bot posts message to Telegram

### Manual Queries

1. User sends command in Telegram
2. OpenClaw receives message via Bot API
3. Command handler executes
4. Response sent back to user

## Configuration

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN_HERE"
    }
  }
}
```

## Research Questions

1. How to get a Telegram bot token?
2. What are the rate limits?
3. How does message formatting work (Markdown)?
4. Can it send files/images?
5. Group chat vs DM behavior?

## Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather](https://t.me/botfather) - Create bots
- OpenClaw Telegram channel implementation
