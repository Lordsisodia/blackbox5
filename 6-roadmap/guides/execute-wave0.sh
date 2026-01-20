#!/bin/bash
# BlackBox5 Wave 0 - Parallel Agent Execution Script

set -e

# Configuration
REPO_ROOT="/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5"
WORKTREE_BASE="/tmp/bb5-wave0"
PROJECT_ID="48ec7737-b706-4817-b86c-5786163a0139"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   BlackBox5 Wave 0 - Parallel Agent Execution         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Create worktree base directory
mkdir -p "$WORKTREE_BASE"

# Clean up any existing worktrees
rm -rf "$WORKTREE_BASE"/* 2>/dev/null || true

echo -e "${YELLOW}Creating 5 isolated git worktrees...${NC}"
echo ""

# Task 1: PLAN-008 - Fix API Mismatches (CRITICAL)
echo -e "${YELLOW}[PLAN-008] Creating worktree for API Mismatches fix...${NC}"
cd "$REPO_ROOT"
git worktree add -b "wave0/PLAN-008-fix-api-mismatches" "$WORKTREE_BASE/PLAN-008-fix-api-mismatches" main 2>/dev/null || git worktree add "$WORKTREE_BASE/PLAN-008-fix-api-mismatches" main

cat > "$WORKTREE_BASE/PLAN-008-fix-api-mismatches/AGENT_TASK.md" <<'EOF'
# BlackBox5 Agent Task - PLAN-008

You are working on the BlackBox5 AI development platform.

## CRITICAL: Fix API Mismatches in main.py

The system CANNOT PROCESS ANY REQUEST due to 3 API parameter mismatches.

### Issues to Fix:

1. **Line 450**: `Task(task_id=...)` → Should be `Task(id=...)`
2. **Line 612**: `execute_wave_based(...)` → Should be `execute_workflow(...)`
3. **Line 558**: `AgentTask(id=...)` → Should be `AgentTask(task_id=...)`
4. **Lines 392, 401, 457, 586, 614**: `task.task_id` → Should be `task.id`

### Steps:

1. Read blackbox5/6-roadmap/03-planned/PLAN-008-fix-critical-api-mismatches.md
2. Fix the 3 API mismatches in main.py
3. Test that system boots and processes requests
4. Document everything in blackbox5/6-roadmap/04-active/PLAN-008-fix-critical-api-mismatches/
5. Update Vibe Kanban task status to "done"

### Success Criteria:
- No TypeError or AttributeError
- System can process simple requests
- All changes documented

Start by reading the plan document!
EOF
echo -e "${GREEN}[PLAN-008] ✓ Worktree created${NC}"

# Task 2: PLAN-007 - Enable 90% Compression
echo -e "${YELLOW}[PLAN-007] Creating worktree for 90% Compression...${NC}"
git worktree add -b "wave0/PLAN-007-enable-90-compression" "$WORKTREE_BASE/PLAN-007-enable-90-compression" main 2>/dev/null || git worktree add "$WORKTREE_BASE/PLAN-007-enable-90-compression" main

cat > "$WORKTREE_BASE/PLAN-007-enable-90-compression/AGENT_TASK.md" <<'EOF'
# BlackBox5 Agent Task - PLAN-007

You are working on the BlackBox5 AI development platform.

## Enable 90% LLMLingua Compression

This saves 90% on token costs ($100 → $10/month).

### Steps:

1. Create HuggingFace account (2 min)
2. Login: `huggingface-cli login` (1 min)
3. Accept LLMLingua license at https://huggingface.co/microsoft/llmlingua-2-x2 (5 min)
4. Verify with: `python3 -c "from llmlingua import LLMLingua; print('Success')"` (5 min)

### Success Criteria:
- LLMLingua imports successfully
- 90% compression active
- Documented in roadmap

Total time: ~15 minutes

Start by reading blackbox5/6-roadmap/03-planned/PLAN-007-enable-90-compression.md
EOF
echo -e "${GREEN}[PLAN-007] ✓ Worktree created${NC}"

# Task 3: PLAN-010 - Add Missing Dependencies
echo -e "${YELLOW}[PLAN-010] Creating worktree for Dependencies...${NC}"
git worktree add -b "wave0/PLAN-010-add-dependencies" "$WORKTREE_BASE/PLAN-010-add-dependencies" main 2>/dev/null || git worktree add "$WORKTREE_BASE/PLAN-010-add-dependencies" main

cat > "$WORKTREE_BASE/PLAN-010-add-dependencies/AGENT_TASK.md" <<'EOF'
# BlackBox5 Agent Task - PLAN-010

You are working on the BlackBox5 AI development platform.

## Add Missing Dependencies to requirements.txt

Fresh installations fail without these dependencies.

### Steps:

1. Audit imports (10 min) - Find all imported packages
2. Update requirements.txt (5 min) - Add: redis, pyyaml, chromadb, neo4j
3. Create requirements-dev.txt (5 min) - Development dependencies
4. Test installation (10 min) - `pip install -r requirements.txt`

### Success Criteria:
- All imports have corresponding packages
- Fresh installation succeeds
- Documented in roadmap

Total time: ~30 minutes

Start by reading blackbox5/6-roadmap/03-planned/PLAN-010-add-missing-dependencies.md
EOF
echo -e "${GREEN}[PLAN-010] ✓ Worktree created${NC}"

# Task 4: PLAN-009 - Fix Statistics Coroutines
echo -e "${YELLOW}[PLAN-009] Creating worktree for Statistics fix...${NC}"
git worktree add -b "wave0/PLAN-009-fix-statistics" "$WORKTREE_BASE/PLAN-009-fix-statistics" main 2>/dev/null || git worktree add "$WORKTREE_BASE/PLAN-009-fix-statistics" main

cat > "$WORKTREE_BASE/PLAN-009-fix-statistics/AGENT_TASK.md" <<'EOF'
# BlackBox5 Agent Task - PLAN-009

You are working on the BlackBox5 AI development platform.

## Fix Statistics Coroutine Warnings

Statistics display shows coroutine objects instead of data.

### Issue:

`get_statistics()` calls async methods without await.

### Steps:

1. Make get_statistics() async (20 min)
2. Add await to async calls (20 min)
3. Update all callers (20 min)

### Success Criteria:
- Statistics display correctly
- No coroutine warnings
- Documented in roadmap

Total time: ~1 hour

Start by reading blackbox5/6-roadmap/03-planned/PLAN-009-fix-statistics-coroutine.md
EOF
echo -e "${GREEN}[PLAN-009] ✓ Worktree created${NC}"

# Task 5: PLAN-005 - Initialize Vibe Kanban
echo -e "${YELLOW}[PLAN-005] Creating worktree for Vibe Kanban...${NC}"
git worktree add -b "wave0/PLAN-005-initialize-vibe-kanban" "$WORKTREE_BASE/PLAN-005-initialize-vibe-kanban" main 2>/dev/null || git worktree add "$WORKTREE_BASE/PLAN-005-initialize-vibe-kanban" main

cat > "$WORKTREE_BASE/PLAN-005-initialize-vibe-kanban/AGENT_TASK.md" <<'EOF'
# BlackBox5 Agent Task - PLAN-005

You are working on the BlackBox5 AI development platform.

## Initialize Vibe Kanban Database

Required before Planning Agent can work.

### Steps:

1. Locate Vibe Kanban installation (15 min)
2. Run migrations (30 min)
3. Create BlackBox5 project (15 min)
4. Test API (30 min)
5. Create columns (15 min)
6. Verify ready (15 min)

### Success Criteria:
- Vibe Kanban database initialized
- BlackBox5 project created
- API working
- Documented in roadmap

Total time: ~2 hours

Start by reading blackbox5/6-roadmap/03-planned/PLAN-005-initialize-vibe-kanban.md
EOF
echo -e "${GREEN}[PLAN-005] ✓ Worktree created${NC}"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   All 5 agent worktrees created successfully!           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Worktree Location:${NC} $WORKTREE_BASE"
echo ""
echo -e "${YELLOW}To start all agents in parallel, run:${NC}"
echo ""
for task in PLAN-008-fix-api-mismatches PLAN-007-enable-90-compression PLAN-010-add-dependencies PLAN-009-fix-statistics PLAN-005-initialize-vibe-kanban; do
    echo "  (cd $WORKTREE_BASE/$task && claude &) \\"
done
echo "  wait"
echo ""
echo -e "${YELLOW}Or start individual agents:${NC}"
echo ""
for task in PLAN-008-fix-api-mismatches PLAN-007-enable-90-compression PLAN-010-add-dependencies PLAN-009-fix-statistics PLAN-005-initialize-vibe-kanban; do
    echo "  cd $WORKTREE_BASE/$task && claude"
done
echo ""
echo -e "${YELLOW}Each worktree is an isolated git branch.${NC}"
echo -e "${YELLOW}Changes will be isolated until merged.${NC}"
echo ""
