#!/bin/bash
# BlackBox5 Parallel Agent Launcher
#
# Launches multiple agents in parallel to work on BlackBox5 improvements
# Each agent is assigned a specific plan and prompted to document everything

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="48ec7737-b706-4817-b86c-5786163a0139"
REPO_ID="b5b86bc2-fbfb-4276-b15e-01496d647a81"
BASE_BRANCH="master"
EXECUTOR="CLAUDE_CODE"

# Task IDs from Vibe Kanban
TASK_008="0425ff12-9d01-433e-a9b0-8ce65b0a08eb"  # PLAN-008: API Mismatches (CRITICAL)
TASK_007="e8e4495b-a3b6-4986-855f-0f4be0b9a959"  # PLAN-007: 90% Compression
TASK_010="a207ee63-5c5e-4c56-9cdc-73cb587d80fc"  # PLAN-010: Dependencies
TASK_009="830c24bb-fef8-48d1-a4de-70d7f6a2f2f7"  # PLAN-009: Statistics
TASK_005="404c9217-cd61-41b9-b855-31b8a1b467df"  # PLAN-005: Vibe Kanban

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   BlackBox5 Parallel Agent Launcher - Wave 0 (Critical)    ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Launching 5 parallel agents for critical fixes...${NC}"
echo ""

# Common prompt for all agents
COMMON_PROMPT="
You are working on the BlackBox5 AI development platform. This is a CRITICAL task.

## MANDATORY: DOCUMENT EVERYTHING

You MUST document all your work in the roadmap:
- Read the plan: blackbox5/6-roadmap/03-planned/[PLAN-NAME]/
- Document findings in blackbox5/6-roadmap/04-active/[PLAN-NAME]/
- Update status in Vibe Kanban as you progress
- Record all decisions, issues, and solutions

## REFERENCE DOCUMENTATION (READ THESE FIRST)

Before starting, you MUST read:
1. blackbox5/6-roadmap/BLACKBOX5-VISION-AND-FLOW.md - What is BlackBox5?
2. blackbox5/6-roadmap/FIRST-PRINCIPLES-ANALYSIS.md - Hidden blockers
3. blackbox5/6-roadmap/EXECUTION-PLAN.md - How to execute
4. Your specific plan in blackbox5/6-roadmap/03-planned/

## WORK APPROACH

1. First, READ and UNDERSTAND the vision and your plan
2. Create a work directory: blackbox5/6-roadmap/04-active/[PLAN-NAME]/
3. Document what you find (issues, decisions, progress)
4. Make changes ONLY after understanding the system
5. Test your changes
6. Document the final state

## QUALITY STANDARDS

- All code must be tested
- All changes must be documented
- All decisions must be rationale
- Update Vibe Kanban card status as you progress

Start by reading the vision document to understand what you're working on!
"

# Function to launch an agent
launch_agent() {
    local task_id=$1
    local plan_name=$2
    local priority=$3

    echo -e "${YELLOW}Launching agent for ${plan_name}...${NC}"

    # Note: This would use the vibe_kanban start_workspace_session tool
    # For now, we're creating a summary file
    cat > /tmp/agent_${task_id}.prompt << EOF
${COMMON_PROMPT}

## YOUR SPECIFIC TASK

Plan: ${plan_name}
Priority: ${priority}
Task ID: ${task_id}

Read your plan file in blackbox5/6-roadmap/03-planned/ for detailed instructions.

Begin by:
1. Reading BLACKBOX5-VISION-AND-FLOW.md
2. Reading your specific plan document
3. Understanding the current state
4. Creating a work directory
5. Starting implementation

Remember: DOCUMENT EVERYTHING in the roadmap!
EOF

    echo -e "  ${GREEN}✓ Agent configuration ready${NC}"
    echo ""
}

# Launch Phase 0 agents (5 parallel agents)
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}WAVE 0: CRITICAL FIXES (3-4 hours)${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}"
echo ""

launch_agent "$TASK_008" "PLAN-008" "🔴🔴 CRITICAL - System won't work without this"
launch_agent "$TASK_007" "PLAN-007" "⚡ QUICK WIN - 15 min for 90% cost reduction"
launch_agent "$TASK_010" "PLAN-010" "⚡ QUICK WIN - 30 min for deployment fixes"
launch_agent "$TASK_009" "PLAN-009" "⚡ QUICK WIN - 1 hour for display fixes"
launch_agent "$TASK_005" "PLAN-005" "🔴 HIGH - 2 hours for Vibe Kanban setup"

echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   All 5 agents configured and ready!                      ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "1. Each agent should read their plan documentation"
echo -e "2. Create work directories in blackbox5/6-roadmap/04-active/"
echo -e "3. Document everything as they work"
echo -e "4. Update Vibe Kanban card status (todo → in_progress → done)"
echo ""
echo -e "${YELLOW}NOTE: These agents will work via Vibe Kanban workspace sessions${NC}"
echo -e "${YELLOW}      The prompts above are saved to /tmp/agent_* files${NC}"
echo ""
