# Scout Report: Hidden Dependencies Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## 1. SHELL SCRIPT DEPENDENCIES (Critical)

**All bb5-* commands depend on engine library:**

Every single bb5 command sources the dry_run.sh library from the engine:

```bash
# In all bin/bb5-* files (12 files):
source "$(dirname "$0")/../2-engine/.autonomous/lib/dry_run.sh" 2>/dev/null || true
```

**Affected files:**
- `/Users/shaansisodia/.blackbox5/bin/bb5-whereami`
- `/Users/shaansisodia/.blackbox5/bin/bb5-link`
- `/Users/shaansisodia/.blackbox5/bin/bb5-discover-context`
- `/Users/shaansisodia/.blackbox5/bin/bb5-populate-template`
- `/Users/shaansisodia/.blackbox5/bin/bb5-goto`
- `/Users/shaansisodia/.blackbox5/bin/bb5-task`
- `/Users/shaansisodia/.blackbox5/bin/bb5-create`
- `/Users/shaansisodia/.blackbox5/bin/bb5-scout-improve`
- `/Users/shaansisodia/.blackbox5/bin/bb5-plan`
- `/Users/shaansisodia/.blackbox5/bin/bb5-timeline`
- `/Users/shaansisodia/.blackbox5/bin/bb5-goal`

**Risk:** HIGH - If `2-engine/.autonomous/lib/dry_run.sh` is moved or deleted, all bb5 commands will fail silently (the `|| true` masks the error).

---

## 2. PYTHON SCRIPT DEPENDENCIES (Critical)

**Agent Improvement Loop scripts hardcode paths to both systems:**

All 5 agent scripts in `2-engine/.autonomous/bin/` have hardcoded dependencies:

```python
# From improvement-loop.py, scout-intelligent.py, planner-prioritize.py,
# executor-implement.py, verifier-validate.py, scout-task-based.py:

PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
ENGINE_DIR = Path.home() / ".blackbox5" / "2-engine"
BIN_DIR = ENGINE_DIR / ".autonomous" / "bin"
REPORTS_DIR = PROJECT_DIR / ".autonomous" / "analysis"
```

**Risk:** HIGH - These scripts assume a specific directory structure that couples them to both systems. They cannot function independently.

---

## 3. RALF EXECUTOR DEPENDENCIES (High)

**ralf-executor-v2 couples engine prompts with project runs:**

```bash
# From bin/ralf-executor-v2:
ENGINE_DIR="${RALF_ENGINE_DIR:-$BASE_DIR/2-engine/.autonomous}"
PROMPT_FILE="$ENGINE_DIR/prompts/system/executor/variations/v2-legacy-based.md"
PROJECT_DIR="${RALF_PROJECT_DIR:-$BASE_DIR/5-project-memory/blackbox5}"
```

The executor reads prompts from engine but writes run data to project.

**Risk:** HIGH - The executor cannot function without both systems present.

---

## 4. HOOK DEPENDENCIES (Medium-High)

**Claude hooks reference both systems:**

```bash
# From .claude/hooks/subagent-tracking.sh:
BB5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"

# From .claude/hooks/session-start-blackbox5.sh:
BB5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"

# From .claude/hooks/timeline-maintenance.sh:
TIMELINE_FILE="$PROJECT_ROOT/5-project-memory/blackbox5/timeline.yaml"
```

**Risk:** MEDIUM - Hooks assume project structure exists at specific relative path.

---

## 5. ENVIRONMENT VARIABLE COUPLING (Medium)

**RALF environment variables bridge both systems:**

Scripts rely on environment variables that may be set by either system:
- `RALF_RUN_DIR` - Set by engine, used by project
- `RALF_RUN_ID` - Set by engine, used by project
- `RALF_PROJECT_DIR` - Points to project
- `RALF_ENGINE_DIR` - Points to engine
- `RALF_BLACKBOX5_DIR` - Points to project root

**Risk:** MEDIUM - Environment variable coupling creates implicit dependencies that are hard to track.

---

## 6. SCOUT-IMPROVE COMMAND DEPENDENCY (High)

**bb5-scout-improve hardcodes engine prompt path:**

```bash
# From bin/bb5-scout-improve:
PROMPT_FILE="$ENGINE_DIR/.autonomous/prompts/ralf-scout-improve.md"
```

**Risk:** HIGH - Command fails if engine prompt is not at exact expected location.

---

## 7. CONFIGURATION DEPENDENCIES (Medium)

**Engine scripts check for project files at runtime:**

```python
# From scout-intelligent.py analyzers:
FILES TO ANALYZE:
- {project_dir}/operations/skill-metrics.yaml
- {project_dir}/operations/skill-usage.yaml
- {project_dir}/.autonomous/runs/*/THOUGHTS.md
```

**Risk:** MEDIUM - Engine scripts assume specific project file structure exists.

---

## 8. IMPLICIT DIRECTORY STRUCTURE ASSUMPTIONS (Medium)

**Relative path assumptions throughout:**

```bash
# bin/bb5-discover-context assumes:
BLACKBOX5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"

# All bb5-* scripts assume:
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
```

**Risk:** MEDIUM - Scripts assume they are installed at `~/.blackbox5/bin/` with specific sibling directories.

---

## Summary Table

| Dependency Type | Files Affected | Risk Level | Description |
|-----------------|----------------|------------|-------------|
| Shell library source | 12 bb5-* commands | HIGH | All source dry_run.sh from engine |
| Python hardcoded paths | 6 engine bin scripts | HIGH | Hardcoded PROJECT_DIR and ENGINE_DIR |
| RALF executor | 1 script | HIGH | Prompts from engine, runs to project |
| Hook paths | 6 hooks | MEDIUM | Hardcoded project paths |
| Environment variables | Multiple | MEDIUM | RALF_* vars bridge systems |
| Scout-improve | 1 command | HIGH | Hardcoded engine prompt path |
| Runtime file checks | Multiple | MEDIUM | Engine checks project files exist |
| Directory structure | All scripts | MEDIUM | Assumes specific installation layout |

---

## Recommendations

1. **Create a configuration layer** - Instead of hardcoded paths, use a config file that both systems read
2. **Decouple the dry_run.sh library** - Copy it to bin/ or make it a standalone package
3. **Use environment variables consistently** - All paths should be overridable via env vars
4. **Create an API/interface boundary** - Engine should expose an API rather than scripts reaching into project files
5. **Add path validation** - Scripts should check paths exist and provide clear error messages
6. **Document the coupling** - Create a DEPENDENCIES.md file documenting these relationships
