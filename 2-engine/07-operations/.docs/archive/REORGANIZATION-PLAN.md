# 07-Operations Reorganization Plan

## Executive Summary

**Current State**: 711 files scattered across `runtime/` and `scripts/` with no clear organization

**Proposed State**: 6 clean categories organized by purpose (commands, workflows, environment, monitoring, validation, utilities)

**Benefit**: Clear, scalable, user-friendly organization

---

## Current Problems

### 1. Confusing Structure
- `runtime/` has 700+ files including scripts, templates, configs, code
- `scripts/` has actual scripts but buried in subdirectories
- No clear distinction between the two folders

### 2. Mixed Purposes
Single folder (`runtime/`) contains:
- Executable commands (autonomous-run.sh, agent-status.sh)
- Templates (prd-templates/, planning/)
- Libraries (lib.sh, lib/, python/)
- Monitoring (monitor.sh, ralph-status.sh)
- Validation (validation/)
- Configuration files
- Git hooks

### 3. Duplicate Categories
- `integration/` and `integrations/` - unclear difference
- `utils/` and `utility/` - duplicates
- `lib/` and `lib.sh` - confusing

### 4. Difficult Navigation
20+ subdirectories with no clear taxonomy. Hard to find what you need.

---

## First-Principles Analysis

### What is "Operations"?

**Operations** = Everything needed to **RUN** the engine in production

### Three Questions:

1. **WHAT do we run?** → Commands (executable scripts)
2. **HOW do we work?** → Workflows (multi-step processes)
3. **WHAT supports it?** → Environment (config, templates, libraries)

### Four Operational Activities:

| Activity | Purpose | Examples |
|----------|---------|----------|
| **Commands** | Execute something | Run agents, start workflows, intervene |
| **Workflows** | Follow a process | Planning, development, discovery |
| **Monitoring** | Check system health | Status checks, logging, health checks |
| **Validation** | Verify things work | Validate system, check constraints |

---

## Proposed Structure

```
07-operations/
├── commands/          # Execute something (126 scripts)
│   ├── run/           # Start/stop operations
│   ├── agents/        # Agent operations
│   ├── system/        # System operations
│   └── specs/         # Spec operations
│
├── workflows/         # Follow a process (89 workflows)
│   ├── planning/      # Planning workflows
│   ├── development/   # Development workflows
│   ├── discovery/     # Research workflows
│   └── memory/        # Memory workflows
│
├── environment/       # Set up where you work (238 files)
│   ├── config/        # Configuration files
│   ├── templates/     # Templates (PRDs, plans, specs)
│   ├── lib/           # Libraries (lib.sh, python/)
│   ├── hooks/         # Git hooks
│   └── services/      # External services (Redis)
│
├── monitoring/        # Check system health (45 scripts)
│   ├── status/        # Status checks
│   ├── logging/       # Log operations
│   ├── health/        # Health checks
│   └── alerts/        # Notifications
│
├── validation/        # Verify things work (67 scripts)
│   ├── check/         # Validation scripts
│   ├── test/          # Test operations
│   └── tools/         # Validation tools
│
└── utilities/         # Helpful tools (146 files)
    ├── git/           # Git operations
    ├── maintenance/   # Maintenance tasks
    ├── setup/         # Setup scripts
    └── tools/         # Development tools
```

---

## Migration Map

### runtime/ → commands/
```
autonomous-run.sh        → commands/run/
autonomous-loop.sh        → commands/run/
ralph-runtime.sh          → commands/run/
agent-status.sh           → commands/agents/
start-agent-cycle.sh      → commands/agents/
new-agent.sh              → commands/agents/
agent-handoff.sh          → commands/agents/
intervene.sh              → commands/system/
monitor.sh                → commands/system/
analyze-response.sh       → commands/system/
circuit-breaker.sh        → commands/system/
spec-create.sh            → commands/specs/
spec-analyze.sh           → commands/specs/
spec-validate.sh          → commands/specs/
```

### runtime/ → workflows/
```
planning/                 → workflows/planning/
testing/                  → workflows/development/
memory/                   → workflows/memory/
questioning/              → workflows/development/questioning/
```

### runtime/ → environment/
```
prd-templates/            → environment/templates/prd-templates/
lib.sh                    → environment/lib/
lib/                      → environment/lib/
python/                   → environment/lib/python/
hooks/                    → environment/hooks/
start-redis.sh            → environment/services/
```

### runtime/ → monitoring/
```
monitor.sh                → monitoring/logging/ (duplicate, decide)
monitoring/               → monitoring/
ralph-status.sh           → monitoring/status/
plan-status.py            → monitoring/status/
ui-cycle-status.py        → monitoring/status/
view-logs.sh              → monitoring/logging/
view-manifest.sh          → monitoring/logging/
```

### runtime/ → validation/
```
validation/               → validation/
testing/ (check scripts)   → validation/test/
```

### scripts/ → utilities/
```
tools/                    → utilities/tools/
utility-scripts/          → utilities/
  ├─ init-project-memory.sh  → utilities/setup/
  ├─ update-index.sh          → utilities/maintenance/
  └─ verify-index.sh          → utilities/maintenance/
```

---

## Special Cases

### ralph/ and ralphy/ (Agent Runtime Data)

**Current location**: `runtime/ralph/`, `runtime/ralphy/`

**Issue**: These are agent session data, not operations

**Recommendation**: Move to `5-project-memory/siso-internal/agents/ralph/`

**Reason**: Runtime data belongs in project memory, not engine operations

### integration/ vs integrations/

**Current**: Two folders with similar names

**Question**: What's the difference?

**Options**:
1. Merge if they're the same
2. Rename to clarify purpose
3. Keep separate if genuinely different

**Need to investigate**: File contents to determine difference

---

## Benefits

### 1. Clear Purpose
Each folder answers "WHY would I use this?"

### 2. User-Friendly
Natural organization:
- "I want to **run** something" → `commands/`
- "I want to **check** status" → `monitoring/`
- "I want to **validate**" → `validation/`

### 3. Scalable
Easy to add new content:
- New command → `commands/{category}/`
- New workflow → `workflows/{category}/`

### 4. No Duplicates
Clear separation eliminates confusion

### 5. Maintainable
Logical structure makes updates easier

---

## Implementation Steps

### Phase 1: Create Structure
```bash
cd 07-operations
mkdir -p commands/{run,agents,system,specs}
mkdir -p workflows/{planning,development,discovery,memory}
mkdir -p environment/{config,templates,lib,hooks,services}
mkdir -p monitoring/{status,logging,health,alerts}
mkdir -p validation/{check,test,tools}
mkdir -p utilities/{git,maintenance,setup,tools}
```

### Phase 2: Move Files
```bash
# Commands
mv runtime/autonomous-run.sh commands/run/
mv runtime/agent-status.sh commands/agents/
# ... (move all command files)

# Workflows
mv runtime/planning/* workflows/planning/
# ... (move all workflow files)

# Environment
mv runtime/prd-templates environment/templates/
mv runtime/lib.sh environment/lib/
# ... (move all environment files)

# Monitoring
mv runtime/monitoring/* monitoring/
# ... (move all monitoring files)

# Validation
mv runtime/validation/* validation/
# ... (move all validation files)

# Utilities
mv scripts/tools/* utilities/tools/
mv scripts/utility-scripts/* utilities/
# ... (move all utility files)
```

### Phase 3: Handle Special Cases
```bash
# Move ralph to project memory
mv runtime/ralph ../../../5-project-memory/siso-internal/agents/
mv runtime/ralphy ../../../5-project-memory/siso-internal/agents/

# Resolve integration/integrations duplicates
# (investigate and merge/rename)
```

### Phase 4: Clean Up
```bash
# Remove empty directories
rm -rf runtime/
rm -rf scripts/

# Verify all files moved
find . -type f | wc -l  # Should still be ~711
```

### Phase 5: Update References
- Update any scripts that reference old paths
- Update documentation
- Test critical operations

---

## Questions Requiring Decisions

### 1. ralph/ and ralphy/
**Question**: Move to project memory or keep in operations?

**Recommendation**: Move to `5-project-memory/siso-internal/agents/` (runtime session data)

### 2. integration vs integrations
**Question**: Merge or keep separate?

**Action Required**: Investigate file contents to determine difference

### 3. monitor.sh duplication
**Question**: `monitor.sh` exists in root and `monitoring/` folder

**Recommendation**: Keep in `monitoring/`, delete from root

---

## Quick Reference Card

After migration, finding files becomes intuitive:

| I want to... | Go to... |
|-------------|----------|
| Run the engine | `commands/run/` |
| Check status | `monitoring/status/` |
| Create a plan | `workflows/planning/` |
| View logs | `monitoring/logging/` |
| Validate system | `validation/check/` |
| Configure system | `environment/config/` |
| Use utilities | `utilities/` |

---

## Risks & Mitigation

### Risk 1: Breaking Script References
**Mitigation**: Update all internal references before moving

### Risk 2: Lost Files During Migration
**Mitigation**: Use `mv` (not `cp`), verify file counts

### Risk 3: Confusion During Transition
**Mitigation**: Document old → new mapping clearly

---

## Success Criteria

✅ All 711 files moved to new locations
✅ No duplicate folders
✅ Clear naming conventions
✅ README explains structure
✅ All critical operations still work
✅ No empty folders (except where intentional)

---

## Timeline Estimate

- Phase 1 (Create structure): 5 minutes
- Phase 2 (Move files): 30 minutes
- Phase 3 (Special cases): 15 minutes
- Phase 4 (Clean up): 10 minutes
- Phase 5 (Update references): 30 minutes

**Total**: ~90 minutes

---

## Next Steps

1. **Review this plan** - Confirm structure makes sense
2. **Answer questions** - Decide on special cases
3. **Approve migration** - Get green light to proceed
4. **Execute migration** - Follow implementation steps
5. **Test operations** - Verify everything still works
6. **Update documentation** - Ensure clarity
