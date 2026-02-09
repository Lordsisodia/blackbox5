#!/bin/bash
# Setup script for BB5 Reporter on VPS

set -e

echo "Setting up BB5 Agent Activity Reporter..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install pyyaml schedule requests -q

# Create directories
echo "Creating directories..."
mkdir -p /opt/blackbox5/agents/moltbot-autonomous/state
mkdir -p /opt/blackbox5/.logs/bb5-reporter

# Copy files
echo "Copying reporter files..."
cp bb5-reporter.py /opt/blackbox5/agents/moltbot-autonomous/
cp bb5-reporter.service /etc/systemd/system/

# Set permissions
chmod +x /opt/blackbox5/agents/moltbot-autonomous/bb5-reporter.py

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

# Enable service
echo "Enabling service..."
systemctl enable bb5-reporter

echo ""
echo "Setup complete!"
echo ""
echo "To start the reporter:"
echo "  sudo systemctl start bb5-reporter"
echo ""
echo "To check status:"
echo "  sudo systemctl status bb5-reporter"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u bb5-reporter -f"
echo ""
echo "To test Telegram:"
echo "  python3 -c \"import requests; requests.post('https://api.telegram.org/bot8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo/sendMessage', json={'chat_id': '7643203581', 'text': '📊 BB5 Reporter test message'})\""
