#!/bin/bash
# Update VPS systemd service to use Python agent loop

cat > /etc/systemd/system/blackbox5-agent.service << 'EOF'
[Unit]
Description=BlackBox5 Autonomous Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/blackbox5
Environment=BB5_DIR=/opt/blackbox5
Environment=HOME=/root
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONUNBUFFERED=1

ExecStart=/usr/bin/python3 /opt/blackbox5/bin/vps-agent-loop.py

Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=3

StandardOutput=append:/var/log/blackbox5-agent.log
StandardError=append:/var/log/blackbox5-agent.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl restart blackbox5-agent

echo "Service updated"
sleep 2
systemctl status blackbox5-agent --no-pager
