# RALF Loop 2 Analysis: Run/Execution Structure Dependencies

## Executive Summary

Loop 1 missed critical dependencies in RALF's run/execution structure. This analysis reveals **deep coupling** between RALF and BlackBox5's run folder structure with hardcoded paths, expected file formats, and state management.

## Critical Findings

### 1. Hardcoded Timestamp-Based Run Directory Pattern

**Files affected:**
- `ralf-loop.sh` lines 71, 72, 156-157
- `legacy-loop.sh` line 12
- `bb5-scout-improve` line 43

**Pattern:**
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RUN_DIR="$PROJECT_AUTONOMOUS/runs/run-$TIMESTAMP"
```

**Impact:** The `run-YYYYMMDD_HHMMSS` format is hardcoded. Any project must adopt this exact convention.

### 2. Mandatory "Big 5" Documentation Files

**phase_gates.py lines 305-311:**
```python
"required_files": [
    "THOUGHTS.md",
    "DECISIONS.md",
    "ASSUMPTIONS.md",
    "LEARNINGS.md",
    "RESULTS.md"
],
```

**Impact:** These 5 files are MANDATORY for phase gate completion. RALF cannot complete without them.

### 3. Nine Different Metadata Files Per Run

| File | Creator | Purpose |
|------|---------|---------|
| `metadata.yaml` | ralf-loop.sh | Loop tracking, timestamps |
| `context_budget.json` | context_budget.py | Token usage tracking |
| `decision_registry.yaml` | decision_registry.py | Decision tracking |
| `tracking.json` | session_tracker.py | File changes, progress |
| `.ralf-metadata` | ralf-loop.sh | Run identification |
| `.hook_initialized` | hooks system | Hook marker |
| `.gate_{phase}_passed` | phase_gates.py | Phase completion |
| `.phase_{phase}_criteria` | phase_gates.py | Criteria verification |
| `.subagent_spawned` | context_budget.py | Sub-agent flag |

### 4. Multi-Stage Initialization Chain

**ralf-loop.sh lines 141-171:**
```bash
init_run() {
    # 1. Initialize telemetry
    TELEMETRY_FILE=$("$TELEMETRY_SCRIPT" init "$PROJECT_AUTONOMOUS")

    # 2. Create run directory
    RUN_DIR="$PROJECT_AUTONOMOUS/runs/run-$TIMESTAMP"
    mkdir -p "$RUN_DIR"

    # 3. Initialize decision registry
    python3 "$DECISION_REGISTRY_SCRIPT" init --run-dir "$RUN_DIR"

    # 4. Initialize context budget
    python3 "$CONTEXT_BUDGET_SCRIPT" init --run-dir "$RUN_DIR"
}
```

**Impact:** Run creation requires 4 subsystems. Missing any breaks run tracking.

### 5. Run-to-Run Dependencies

**scout-intelligent.py lines 86-91:**
```python
FILES TO ANALYZE:
- {project_dir}/.autonomous/runs/*/THOUGHTS.md (last 5 runs)
- {project_dir}/.autonomous/runs/*/LEARNINGS.md (last 5 runs)
```

**planner-prioritize.py lines 25, 307-308:**
```python
DEFAULT_SCOUT_REPORT = PROJECT_DIR / ".autonomous" / "analysis" / "scout-reports" / "scout-report-intelligent-20260205-aggregated.yaml"
```

**Impact:** The improvement loop depends on files from previous runs. Without historical data, the loop cannot function.

### 6. No Graceful Degradation

**improvement-loop.py lines 183-186:**
```python
report_dir = REPORTS_DIR / "loop-reports"
report_dir.mkdir(parents=True, exist_ok=True)  # Only creates subdirectories
```

**Impact:** If `runs/` directory doesn't exist, RALF will fail.

### 7. Hidden Dependencies Found

- **Telemetry system** - Creates JSON files in `.autonomous/telemetry/`
- **Session logging** - All output tee'd to `ralf-session-$TIMESTAMP.log`
- **Decision registry template** - Requires template from `prompt-progression/versions/v2.3/templates/`
- **Hook system** - Checks for `$ENGINE_DIR/lib/ralf_hooks.sh`

## Impact on Portability

| Dependency | Portability Impact |
|------------|-------------------|
| Hardcoded `~/.blackbox5` path | Cannot run outside user's home |
| `5-project-memory/blackbox5` subpath | Project must be named "blackbox5" |
| `.autonomous/runs/` structure | Must use BB5 directory layout |
| 5 required documentation files | All 5 must be created and filled |
| 9+ metadata files | Each has specific format |
| Timestamp format `YYYYMMDD_HHMMSS` | Must match exactly |
| Scout→Planner→Executor→Verifier chain | All 4 must share structure |

## Decoupling Recommendations

### Immediate (High Priority)
1. **Configuration file** - Create `ralf-config.yaml` for run directory path, required files, metadata formats
2. **Run directory factory** - Abstract creation into pluggable interface
3. **Documentation template system** - Make "Big 5" files configurable

### Medium Priority
4. **Metadata abstraction layer** - Unified metadata API
5. **Phase gate plugin system** - Make gates optional and configurable
6. **Telemetry abstraction** - Support multiple backends

### Long Term
7. **Run lifecycle hooks** - Formalize hook system
8. **Historical run adapter** - Adapter pattern for previous runs

## Summary

Loop 1 missed the depth of RALF's coupling to BB5's run structure. The system has **9+ metadata files**, **hardcoded paths**, **mandatory documentation**, and **run-to-run dependencies** that make it impossible to port without significant refactoring.
