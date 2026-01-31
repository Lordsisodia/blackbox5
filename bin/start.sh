#!/bin/bash
# Blackbox5 Startup Script
# Usage: ./start.sh [options]
#
# Options:
#   --help           Show this help message

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory (bin/) and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENGINE_DIR="$PROJECT_ROOT/2-engine/core"

# Parse options
START_API=true

case "${1:-}" in
    --help|-h)
        echo "Blackbox5 Startup Script"
        echo ""
        echo "Usage: ./start.sh"
        echo ""
        echo "Starts the Blackbox5 API server."
        echo ""
        exit 0
        ;;
esac

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           🚀 BLACKBOX5 STARTUP SEQUENCE             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Update catalog if needed
echo -e "${YELLOW}📋 Checking catalog...${NC}"
if [ ! -f "$PROJECT_ROOT/CATALOG.md" ] || [ "$PROJECT_ROOT/2-engine" -nt "$PROJECT_ROOT/CATALOG.md" ]; then
    echo -e "${YELLOW}📝 Updating catalog...${NC}"
    python3 "$PROJECT_ROOT/scripts/generate_catalog.py" > "$PROJECT_ROOT/CATALOG.md" 2>/dev/null
    echo -e "${GREEN}✅ Catalog updated${NC}"
else
    echo -e "${GREEN}✅ Catalog current${NC}"
fi
echo ""

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Check prerequisites
echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# Start Blackbox5 API
if [ "$START_API" = true ]; then
    echo -e "${YELLOW}⚙️  Starting Blackbox5 API Server...${NC}"

    if check_port 8000; then
        echo -e "${YELLOW}⚠️  Port 8000 already in use. API may already be running.${NC}"
    else
        cd "$ENGINE_DIR"

        # Check Python dependencies
        if [ -f "requirements.txt" ]; then
            echo -e "${YELLOW}📦 Checking Python dependencies...${NC}"
            pip3 install -q -r requirements.txt 2>/dev/null || true
        fi

        # Start API in background
        echo -e "${GREEN}✅ Starting API on http://localhost:8000${NC}"
        echo -e "${GREEN}   API Docs: http://localhost:8000/docs${NC}"
        python3 -m core.interface.api.main > /tmp/blackbox5-api.log 2>&1 &
        API_PID=$!
        echo "   API PID: $API_PID"
        echo "   Logs: /tmp/blackbox5-api.log"

        # Wait a bit for API to start
        sleep 3

        if check_port 8000; then
            echo -e "${GREEN}✅ API started successfully!${NC}"
        else
            echo -e "${YELLOW}⚠️  API starting... check logs if needed${NC}"
        fi
    fi
    echo ""
fi

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              🎉 BLACKBOX5 IS RUNNING!                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$START_API" = true ]; then
    echo -e "${GREEN}🌐 API Server:${NC}    http://localhost:8000"
    echo -e "${GREEN}📚 API Docs:${NC}      http://localhost:8000/docs"
    echo ""
fi

echo -e "${YELLOW}💡 Quick Commands:${NC}"
echo -e "   ${BLUE}curl http://localhost:8000/health${NC}           # Check API health"
echo -e "   ${BLUE}curl http://localhost:8000/agents${NC}           # List all agents"
echo -e "   ${BLUE}tail -f /tmp/blackbox5-api.log${NC}              # View API logs"
echo ""

if [ ! -z "${API_PID:-}" ]; then
    echo -e "${YELLOW}Press Ctrl+C to stop the API server, or run:${NC}"
    echo -e "   ${BLUE}kill $API_PID${NC}"
    echo ""

    # Handle graceful shutdown
    trap "echo -e '${YELLOW}🛑 Stopping Blackbox5...${NC}'; kill $API_PID 2>/dev/null; echo -e '${GREEN}✅ Done${NC}'; exit 0" SIGINT SIGTERM

    # Keep script running
    wait
fi
