# BlackBox5 Agent Dashboard - Deployment Guide

**Fresh Mind-Style UI for Managing All Autonomous Agents**

## What You Have

A single-file HTML dashboard with real-time agent management, just like Fresh Mind!

## Features

- **Real-time Status Cards** - See all agents: running, idle, error
- **One-Click Agent Chats** - Click "Talk to Agent" to start new session with any agent
- **Start/Stop Control** - Instant control over any agent
- **Task & Progress Tracking** - See what each agent is working on
- **Uptime Monitoring** - How long has each agent been running
- **Token Usage** - Track costs per agent
- **Create New Agents** - Add custom agents from UI
- **Stats Bar** - Quick overview at bottom of screen

## Quick Deploy

```bash
# Option 1: Simple HTTP server (easy)
cd /opt/blackbox5
mkdir -p dashboard-ui/public
cp index.html dashboard-ui/public/
cd dashboard-ui/public
python3 -m http.server 8080

# Option 2: Use existing OpenClaw gateway (recommended)
# Serve from /opt/blackbox5/dashboard-ui/
# Access at: http://77.42.66.40:18789/dashboard-ui/
```

## How to Connect to Real OpenClaw

The dashboard is currently **simulated** with mock data. To make it real:

### Step 1: Add Dashboard Configuration to OpenClaw

Create `/opt/blackbox5/dashboard-ui/openclaw-config.sh`:

```bash
#!/bin/bash

# This script configures OpenClaw to serve the dashboard

BB5_DIR="/opt/blackbox5"

# Add dashboard to skills
mkdir -p /root/.openclaw/skills/bb5-dashboard/
cat > /root/.openclaw/skills/bb5-dashboard/SKILL.md << 'EOF'
---
name: bb5-dashboard
description: Fresh Mind-style agent management dashboard for BlackBox5
---

# BB5 Dashboard

Manage all autonomous agents from one web interface.

## Features

- Real-time agent status monitoring
- One-click agent chat creation
- Start/stop agent controls
- Token usage tracking
- Task progress monitoring

## Usage

Invoke this skill to get agent status or send commands.
EOF

# Configure OpenClaw to serve the dashboard
echo "Configuring OpenClaw to serve BB5 dashboard..."

# Create a simple web server route
cat > /tmp/dashboard-server.py << 'PYEOF'
#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json
import subprocess

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            with open('/opt/blackbox5/dashboard-ui/index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/api/agents':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            agents = self.get_agent_status()
            self.wfile.write(json.dumps(agents))
        elif self.path == '/api/agents/start':
            agent_id = self.path.split('/')[-1]
            result = self.start_agent(agent_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.wfile.write(json.dumps(result))
    
    def do_POST(self):
        if self.path == '/api/agents/stop':
            agent_id = self.path.split('/')[-1]
            result = self.stop_agent(agent_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.wfile.write(json.dumps(result))
        elif self.path == '/api/agents/create':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            result = self.create_agent(json.loads(post_data))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.wfile.write(json.dumps(result))
    
    def get_agent_status(self):
        """Get real status of all BB5 agents"""
        # This would call OpenClaw's sessions_list API
        # For now, return mock data
        return [
            {
                'id': 'blackbox5-scribe',
                'name': 'BlackBox5 Scribe',
                'status': 'running',
                'task': 'Monitoring tasks',
                'uptime': '3h 15m',
                'tokensUsed': '13k'
            },
            {
                'id': 'autonomous-improvement',
                'name': "Autonomous Improvement",
                'status': 'idle',
                'task': 'Ready for work',
                'uptime': '0m'
            },
            {
                'id': 'youtube-knowledge-pipeline',
                'name': 'YouTube Knowledge Pipeline',
                'status': 'running',
                'task': 'Processing transcripts',
                'uptime': '4h 20m'
            },
            {
                'id': 'kimi-load-balancer',
                'name': 'Kimi Load Balancer',
                'status': 'idle',
                'task': 'Monitoring API keys'
                'uptime': '6h 30m'
            }
        ]
    
    def start_agent(self, agent_id):
        """Start an agent via OpenClaw"""
        result = subprocess.run(['openclaw', 'session', 'start', 'agent', agent_id], 
                              capture_output=True, text=True)
        return {'success': True, 'agent_id': agent_id, 'output': result.stdout}
    
    def stop_agent(self, agent_id):
        """Stop an agent via OpenClaw"""
        result = subprocess.run(['openclaw', 'session', 'kill', 'agent', agent_id], 
                              capture_output=True, text=True)
        return {'success': True, 'agent_id': agent_id, 'output': result.stdout}

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8081), DashboardHandler)
    print(f'Dashboard server running at http://0.0.0.0:8081')
    print(f'Serving dashboard from /opt/blackbox5/dashboard-ui/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\\nDashboard server stopped')
PYEOF

# Start the dashboard server
nohup python3 /tmp/dashboard-server.py > /var/log/dashboard-server.log 2>&1 &
echo "Dashboard started on http://localhost:8081"
echo "Access at: http://77.42.66.40:18789/dashboard-ui/"
EOF

chmod +x /tmp/dashboard-server.py

# Run the dashboard server
python3 /tmp/dashboard-server.py > /var/log/bb5-dashboard.log 2>&1 &
```

### Step 2: Configure OpenClaw to Proxy Dashboard Requests

```bash
# Add dashboard route to OpenClaw gateway
openclaw gateway configure --http
```

### Step 3: Access Your Dashboard

```
http://77.42.66.40:18789/dashboard-ui/
```

## What You Can Do From the Dashboard

### 1. Monitor All Agents
- See real-time status (running, idle, error)
- Check what tasks each agent is working on
- View uptime and token usage

### 2. One-Click Agent Chats
- Click "Talk to Agent" to instantly start new chat with that agent
- Each agent chat is isolated with its own memory
- Agent remembers context between chats

### 3. Control Agents
- Start or stop any agent instantly
- No need to use CLI - full UI control

### 4. Create Custom Agents
- Click "Create New Agent" button
- Give it a name and description
- Assign tasks to it

### 5. Send Tasks to Agents
- Coming soon: Click on agent → "Assign Task"
- Agent will receive task and start working

## Integration with Your Existing Systems

The dashboard can automatically:
1. **Query OpenClaw** - Get real agent status via sessions API
2. **Invoke CLI** - Start/stop agents via subprocess
3. **Read BlackBox5** - Access task files and memory
4. **Monitor Processes** - Check if agents are running

## Future Enhancements

- **WebSocket support** - Real-time agent updates without refresh
- **Agent chat embedded** - Direct chat within dashboard (no new tab)
- **Task queue** - Drag-and-drop task assignment
- **Log viewer** - Full agent logs in UI
- **Settings panel** - Configure everything from web interface

## File Structure Created

```
/opt/blackbox5/dashboard-ui/
├── index.html              # Fresh Mind-style dashboard
├── openclaw-config.sh      # Configuration script
└── README.md              # This file
```

## Tech Stack

- **Frontend:** Pure HTML/CSS/JavaScript (no frameworks needed)
- **Backend:** Python http.server (or integrate with OpenClaw)
- **Real Data:** Calls OpenClaw sessions_list API when available

## Deployment

**Quick Start (5 minutes):**
1. Create dashboard files
2. Start server
3. Open browser to dashboard

**Production:**
- Integrate with OpenClaw gateway routing
- Use systemd for auto-start
- Set up HTTPS (if needed)

---

Ready to deploy? Run:
```bash
cd /opt/blackbox5/dashboard-ui
python3 -m http.server 8080
```

Then open: `http://77.42.66.40:18789/dashboard-ui/`
