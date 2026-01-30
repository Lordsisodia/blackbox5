#!/bin/bash
# RALF - Classic Ralph Technique
# Non-stop autonomous improvement loop for blackbox5
# Usage: ./ralf-loop.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  RALF - Recursive Autonomous Learning Framework${NC}"
echo -e "${BLUE}  Non-stop self-improvement mode${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Working directory: $(pwd)"
echo "Starting autonomous loop..."
echo "Press Ctrl+C to stop"
echo ""

LOOP_COUNT=0

while true; do
    LOOP_COUNT=$((LOOP_COUNT + 1))

    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  LOOP $LOOP_COUNT - $(date)${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Pull latest before each run
    echo -e "${BLUE}→ Pulling latest from GitHub...${NC}"
    git pull origin $(git branch --show-current) 2>/dev/null || true
    echo ""

    # Run RALF with the prompt
    echo -e "${BLUE}→ Executing RALF prompt...${NC}"
    echo ""

    # The classic Ralph technique: cat prompt | claude -p
    if ! cat ralf.md | claude -p --dangerously-skip-permissions; then
        echo -e "${RED}✗ RALF execution failed${NC}"
        echo "Waiting 30 seconds before retry..."
        sleep 30
        continue
    fi

    echo ""
    echo -e "${GREEN}✓ Loop $LOOP_COUNT complete${NC}"

    # Push any changes
    if ! git diff --quiet HEAD 2>/dev/null; then
        echo -e "${BLUE}→ Committing changes...${NC}"
        git add -A
        git commit -m "ralf: [$(date +%Y%m%d-%H%M%S)] autonomous improvements" || true

        echo -e "${BLUE}→ Pushing to GitHub...${NC}"
        git push origin $(git branch --show-current) 2>/dev/null || echo "Push failed, will retry"
    fi

    echo ""
    echo -e "${BLUE}→ Sleeping 5 seconds before next loop...${NC}"
    sleep 5
    echo ""
done
