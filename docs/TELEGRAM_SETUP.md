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
