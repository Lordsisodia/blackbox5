#!/bin/bash

BB5_DIR="/opt/blackbox5"
GATEWAY_DIR="/opt/blackbox5/gateway"
PORT=8001

echo "🚀 Starting BlackBox5 Gateway and Dashboard..."

# Install dependencies
cd "$GATEWAY_DIR"
if [ ! -d "node_modules" ]; then
    npm install express cors axios
fi

# Start the gateway server
nohup node server.js > /var/log/bb5-gateway.log 2>&1 &
GATEWAY_PID=$!

echo "✅ Gateway started on port $PORT"
echo "   PID: $GATEWAY_PID"
echo "   Dashboard: http://77.42.66.40:$PORT/"
echo ""
echo "📊 Gateway is now running!"
echo "   It integrates with OpenClaw's 'openclaw session start agent:<id>' command"
echo "   Dashboard UI is at the URL above"
echo ""
echo "💡 Ready to manage all your autonomous agents!"
echo "   - Create tasks with + button"
echo "   - Assign tasks to specific agents"
echo "   - Start/Stop agents instantly"
echo "   - View agent status in real-time"
echo ""
echo "🔧 Gateway log: tail -f /var/log/bb5-gateway.log"
