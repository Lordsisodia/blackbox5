# TASK-ARCH-067: Decouple 4 bash agents from hardcoded paths

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-06
**Completed:** 2026-02-06

## Objective
Remove hardcoded `/opt/ralf` paths from all 4 bash agents and implement environment variable support with auto-detection fallback.

## Success Criteria
- [x] No hardcoded `/opt/ralf` paths in agent scripts
- [x] Agents use `BB5_PROJECT_ROOT` environment variable
- [x] Auto-detection fallback from script location
- [x] Backward compatibility maintained
- [x] .env.example created documenting required variables

## Changes Made

### 1. scout-agent.sh
- Replaced `PROJECT_ROOT="/opt/ralf"` with environment variable detection
- Added auto-detection logic: traverses 5 levels up from script location

### 2. analyzer-agent.sh
- Replaced `PROJECT_ROOT="/opt/ralf"` with environment variable detection
- Added auto-detection logic: traverses 5 levels up from script location

### 3. planner-agent.sh
- Replaced `PROJECT_ROOT="/opt/ralf"` with environment variable detection
- Added auto-detection logic: traverses 5 levels up from script location

### 4. github-analysis-pipeline.sh
- Replaced `PROJECT_ROOT="/opt/ralf"` with environment variable detection
- Added auto-detection logic: traverses 4 levels up from script location

### 5. .env.example
- Created at `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/.env.example`
- Documents `BB5_PROJECT_ROOT` environment variable
- Includes additional configuration options for future use

## Implementation Pattern

Each agent now uses this pattern:
```bash
# Determine project root: use env var, or auto-detect from script location
if [ -n "$BB5_PROJECT_ROOT" ]; then
    PROJECT_ROOT="$BB5_PROJECT_ROOT"
else
    # Auto-detect from script location
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
fi
```

## Files Modified
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/scout/scout-agent.sh`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/analyzer/analyzer-agent.sh`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/planner-agent.sh`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/github-analysis-pipeline.sh`

## Files Created
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/.env.example`

## Validation
- All scripts pass `bash -n` syntax check
- No remaining hardcoded `/opt/ralf` paths (except in .env.example as commented example)
- All scripts reference `BB5_PROJECT_ROOT` environment variable

## Rollback Strategy
Revert the commits or restore from backup:
```bash
git checkout HEAD~1 -- 5-project-memory/blackbox5/.autonomous/agents/
```
