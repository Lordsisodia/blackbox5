# Simple Gateway Server - For BlackBox5 Dashboard

**A personal gateway that gives us full control over agent management**

## What This Does

- Serves the dashboard at `http://77.42.66.40:8081/`
- Provides REST API for agent operations (start/stop/status)
- Integrates with OpenClaw's `sessions_spawn` to create agent chats
- Shows real-time agent status
- No OpenClaw dependencies - complete control

## Quick Start

```bash
# Install dependencies (already have node)
cd /opt/blackbox5/gateway
npm install express cors axios socket.io

# Start server
nohup node server.js > /var/log/bb5-gateway.log 2>&1 &

# Access dashboard
# http://77.42.66.40:8081/
```

## API Endpoints

```
GET  /api/agents
POST /api/agents/:id/start
POST /api/agents/:id/stop
GET /api/status
```

## Integration with OpenClaw

The gateway calls `openclaw session start agent:<agentId>` which creates new isolated sessions for each agent. This is much cleaner than trying to hack OpenClaw's UI.

## Deployment

1. **Option 1 (Quick)**: Simple HTTP server
   - Easy to deploy
   - Fast and reliable
   - No dependencies beyond Node.js

2. **Option 2 (Recommended)**: Use existing OpenClaw CLI
   - Use `openclaw session` to create agent chats
   - All agents share same OpenClaw workspace
   - Dashboard just views sessions
   - Most robust option

I recommend **Option 2** - let's use what we have rather than fighting OpenClaw's limitations.

What do you think, SISO? Want to try Option 2 (integrate with existing OpenClaw) or Option 1 (standalone server)?
