#!/bin/bash
# Send an immediate BB5 activity update to Telegram
# Usage: ./send-update.sh [hours]

HOURS=${1:-1}
TOPIC_ID=${2:-}  # Optional: Telegram topic ID for Blackbox channel

cd /opt/blackbox5

# Run the reporter in one-shot mode
python3 << EOF
import sys
sys.path.insert(0, '/opt/blackbox5/agents/moltbot-autonomous')

from bb5_reporter import BB5Reporter

reporter = BB5Reporter()
reporter.send_periodic_update(hours=$HOURS, topic_id=${TOPIC_ID:-None})
print(f"Update sent for last $HOURS hour(s)")
EOF
