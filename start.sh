#!/bin/bash
# Blackbox5 Startup Script
# Usage: ./start.sh [options]
#
# Options:
#   --api-only       Start only the API server
#   --gui-only       Start only Vibe Kanban GUI
#   --full           Start both API and GUI (default)
#   --help           Show this help message

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_DIR="$SCRIPT_DIR/2-engine/01-core"
GUI_DIR="$SCRIPT_DIR/3-gui/vibe-kanban"

# Parse options
START_API=true
START_GUI=true

case "${1:-}" in
    --api-only)
        START_GUI=false
        ;;
    --gui-only)
        START_API=false
        ;;
    --full)
        START_API=true
        START_GUI=true
        ;;
    --help|-h)
        echo "Blackbox5 Startup Script"
        echo ""
        echo "Usage: ./start.sh [option]"
        echo ""
        echo "Options:"
        echo "  --api-only       Start only the API server (port 8000)"
        echo "  --gui-only       Start only Vibe Kanban GUI (port 3000)"
        echo "  --full           Start both API and GUI (default)"
        echo "  --help, -h       Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./start.sh              # Start everything"
        echo "  ./start.sh --api-only   # Start just the API"
        echo "  ./start.sh --gui-only   # Start just the GUI"
        exit 0
        ;;
esac

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           🚀 BLACKBOX5 STARTUP SEQUENCE             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Update catalog if needed
echo -e "${YELLOW}📋 Checking catalog...${NC}"
if [ ! -f "CATALOG.md" ] || [ "2-engine" -nt "CATALOG.md" ]; then
    echo -e "${YELLOW}📝 Updating catalog...${NC}"
    python3 scripts/generate_catalog.py > CATALOG.md 2>/dev/null
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

if ! command -v pnpm &> /dev/null && [ "$START_GUI" = true ]; then
    echo -e "${YELLOW}⚠️  pnpm not found. Attempting to install...${NC}"
    npm install -g pnpm
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# Start Vibe Kanban GUI
if [ "$START_GUI" = true ]; then
    echo -e "${YELLOW}🎨 Starting Vibe Kanban GUI...${NC}"

    if check_port 3000; then
        echo -e "${YELLOW}⚠️  Port 3000 already in use. GUI may already be running.${NC}"
    else
        cd "$GUI_DIR"

        # Install dependencies if needed
        if [ ! -d "node_modules" ]; then
            echo -e "${YELLOW}📦 Installing GUI dependencies...${NC}"
            pnpm install --silent
        fi

        # Start GUI in background
        echo -e "${GREEN}✅ Starting GUI on http://localhost:3000${NC}"
        pnpm run dev > /tmp/vibe-kanban.log 2>&1 &
        GUI_PID=$!
        echo "   GUI PID: $GUI_PID"
        echo "   Logs: /tmp/vibe-kanban.log"

        # Wait a bit for GUI to start
        sleep 3

        if check_port 3000; then
            echo -e "${GREEN}✅ GUI started successfully!${NC}"
        else
            echo -e "${YELLOW}⚠️  GUI starting... check logs if needed${NC}"
        fi
    fi
    echo ""
fi

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
        python3 -m interface.api.main > /tmp/blackbox5-api.log 2>&1 &
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

if [ "$START_GUI" = true ]; then
    echo -e "${GREEN}🎨 Vibe Kanban:${NC}   http://localhost:3000"
    echo ""
fi

echo -e "${YELLOW}💡 Quick Commands:${NC}"
echo -e "   ${BLUE}curl http://localhost:8000/health${NC}           # Check API health"
echo -e "   ${BLUE}curl http://localhost:8000/agents${NC}           # List all agents"
echo -e "   ${BLUE}tail -f /tmp/blackbox5-api.log${NC}              # View API logs"
echo -e "   ${BLUE}tail -f /tmp/vibe-kanban.log${NC}                # View GUI logs"
echo ""

if [ ! -z "${GUI_PID:-}" ] || [ ! -z "${API_PID:-}" ]; then
    echo -e "${YELLOW}Press Ctrl+C to stop all services, or run:${NC}"
    echo -e "   ${BLUE}kill $GUI_PID $API_PID${NC} 2>/dev/null"
    echo ""

    # Handle graceful shutdown
    trap "echo -e '${YELLOW}🛑 Stopping Blackbox5...${NC}'; kill $GUI_PID $API_PID 2>/dev/null; echo -e '${GREEN}✅ Done${NC}'; exit 0" SIGINT SIGTERM

    # Keep script running
    wait
fi
