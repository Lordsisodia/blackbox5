#!/bin/bash
#
# Setup Autonomous Improvement Loops for BlackBox5
#

set -e

BB5_HOME="/opt/blackbox5"
AUTONOMOUS_DIR="$BB5_HOME/.autonomous"

echo "🔧 Setting up autonomous improvement loops..."

# Create directories
mkdir -p "$AUTONOMOUS_DIR/logs"
mkdir -p "$AUTONOMOUS_DIR/metrics"
mkdir -p "$AUTONOMOUS_DIR/runs"
mkdir -p "$BB5_HOME/autonomous"
mkdir -p "$BB5_HOME/config"
mkdir -p "$BB5_HOME/agents/moltbot-autonomous"
mkdir -p "$BB5_HOME/dashboard-ui"

# Make scripts executable
chmod +x "$BB5_HOME/autonomous/improve-blackbox5.sh"

# Create initial log file
if [ ! -f "$AUTONOMOUS_DIR/improvement-log.md" ]; then
    cat > "$AUTONOMOUS_DIR/improvement-log.md" << 'EOF'
# Autonomous Improvement Log

This log tracks all autonomous improvement cycles for BlackBox5.

EOF
fi

# Add cron job
echo ""
echo "📅 Adding cron job (every 20 minutes)..."
CRON_CMD="*/20 * * * * $BB5_HOME/autonomous/improve-blackbox5.sh >> $AUTONOMOUS_DIR/improvement-log.md 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "improve-blackbox5.sh"; then
    echo "⚠️  Cron job already exists, skipping..."
else
    # Add cron job
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Cron job added successfully"
fi

echo ""
echo "✅ Autonomous improvement loops setup complete!"
echo ""
echo "Next steps:"
echo "  1. Monitor first improvement cycle: tail -f $AUTONOMOUS_DIR/improvement-log.md"
echo "  2. Check metrics: $AUTONOMOUS_DIR/metrics/"
echo "  3. View dashboard: http://localhost:8080 (if running)"
