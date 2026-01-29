#!/bin/bash
# Ralph Autonomous Agent - Status Check
# Usage: ./status.sh

RALPH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$RALPH_DIR/STATE"
LOG_DIR="$RALPH_DIR/LOGS"
PID_FILE="$STATE_DIR/ralph.pid"
CURRENT_SESSION="$STATE_DIR/current-session.yaml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              Ralph Autonomous Agent Status                 ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running
if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE" 2>/dev/null || echo "")
    if [[ -n "$PID" ]] && ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}Status: RUNNING${NC}"
        echo -e "  PID: $PID"
    else
        echo -e "${YELLOW}Status: STOPPED (stale PID file)${NC}"
    fi
else
    echo -e "${RED}Status: NOT RUNNING${NC}"
fi
echo ""

# Current session info
if [[ -f "$CURRENT_SESSION" ]]; then
    echo -e "${BLUE}Current Session:${NC}"
    cat "$CURRENT_SESSION" | sed 's/^/  /'
    echo ""
fi

# Git branch
echo -e "${BLUE}Git Branch:${NC}"
CURRENT_BRANCH=$(git -C "$RALPH_DIR" branch --show-current 2>/dev/null || echo "unknown")
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
    echo -e "  ${RED}⚠️  $CURRENT_BRANCH (FORBIDDEN)${NC}"
else
    echo -e "  ${GREEN}✓ $CURRENT_BRANCH (allowed)${NC}"
fi
echo ""

# API Status
echo -e "${BLUE}API Status:${NC}"
if command -v claude &> /dev/null; then
    echo -e "  ${GREEN}✓ GLM (claude)${NC}"
else
    echo -e "  ${RED}✗ GLM (claude) - not found${NC}"
fi

if command -v cso-kimi &> /dev/null; then
    echo -e "  ${GREEN}✓ Kimi (cso-kimi)${NC}"
else
    echo -e "  ${RED}✗ Kimi (cso-kimi) - not found${NC}"
fi
echo ""

# Recent logs
echo -e "${BLUE}Recent Sessions:${NC}"
if [[ -d "$LOG_DIR/sessions" ]]; then
    ls -1t "$LOG_DIR/sessions" 2>/dev/null | head -5 | while read f; do
        echo "  - $f"
    done
else
    echo "  No sessions found"
fi
echo ""

# Recent errors
echo -e "${BLUE}Recent Errors:${NC}"
if [[ -d "$LOG_DIR/errors" ]]; then
    ERROR_COUNT=$(ls -1 "$LOG_DIR/errors" 2>/dev/null | wc -l)
    if [[ $ERROR_COUNT -gt 0 ]]; then
        echo -e "  ${YELLOW}$ERROR_COUNT error log(s) found${NC}"
        ls -1t "$LOG_DIR/errors" 2>/dev/null | head -3 | while read f; do
            echo "    - $f"
        done
    else
        echo -e "  ${GREEN}No errors${NC}"
    fi
else
    echo "  No error logs"
fi
echo ""

# Quick actions
echo -e "${BLUE}Quick Actions:${NC}"
echo "  ./start-ralph.sh [setup|feature|idea|test|full]"
echo "  ./stop-ralph.sh"
echo "  tail -f $LOG_DIR/sessions/latest.log"
echo ""
