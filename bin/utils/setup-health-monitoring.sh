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
echo "Installing dependencies..."
pip3 install --user pyyaml rich click python-telegram-bot 2>/dev/null || pip3 install pyyaml rich click python-telegram-bot

# Create config from template
if [ ! -f ~/.blackbox5/config/watch-config.yaml ]; then
    cat > ~/.blackbox5/config/watch-config.yaml << 'EOF'
daemon:
  check_interval_seconds: 30
  health_score_threshold: 60
  alert_cooldown_seconds: 300

checks:
  agents:
    enabled: true
    heartbeat_timeout_seconds: 120
    alert_on_stuck: true

  queue:
    enabled: true
    alert_on_backlog_threshold: 20
    alert_on_empty: false

  tasks:
    enabled: true
    stuck_task_multiplier: 2.0

  system:
    enabled: true
    cpu_warning: 80
    cpu_critical: 95
    memory_warning: 80
    memory_critical: 95

alerts:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
    min_severity: warning

  webhook:
    enabled: false
    url: "${WEBHOOK_URL}"
    min_severity: critical

logging:
  level: INFO
  file: ~/.blackbox5/.autonomous/health/watch.log
  max_size_mb: 100
  backup_count: 5
EOF
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
echo "Initializing database..."
python3 -c "from health_monitor.database import init_database; init_database()" 2>/dev/null || echo "Database will be initialized on first run"

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit ~/.blackbox5/config/watch.env with your Telegram credentials"
echo "2. Edit ~/.blackbox5/config/watch-config.yaml with your preferences"
echo "3. Test: bb5-health"
echo "4. Start daemon: bb5-watch start"
echo "5. Enable auto-start: sudo systemctl enable bb5-watch@$USER"
echo ""
echo "See docs/VPS_DEPLOYMENT.md for full deployment instructions"
