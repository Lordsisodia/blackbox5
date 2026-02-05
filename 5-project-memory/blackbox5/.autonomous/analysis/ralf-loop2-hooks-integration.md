# RALF Loop 2 Analysis: Hooks and Triggers Integration

## Executive Summary

RALF has **deep, structural coupling to Claude Code hooks** that Loop 1 missed. The coupling is not just configuration—it's **behavioral assumptions** baked into the entire RALF architecture. Without Claude Code hooks, RALF cannot function properly.

## Critical Findings

### 1. Critical Hardcoded Hook Paths

From `.claude/settings.json`:

| Hook Event | Script Path | Purpose | Impact if Missing |
|------------|-------------|---------|-------------------|
| SessionStart | `session-start-blackbox5.sh` | Load agent context | Agent runs without context |
| SessionStart | `session-start-navigation.sh` | Discover hierarchy | Navigation commands fail |
| PreToolUse | `pre-tool-security.py` | Security validation | No security enforcement |
| PreToolUse | `pre-tool-validation.sh` | Structure validation | Files written without validation |
| PostToolUse | `timeline-maintenance.sh` | Auto-update timeline | Timeline becomes stale |
| PostToolUse | `context-synchronization.sh` | Sync goal progress | State desynchronization |
| SubagentStart/Stop | `subagent-tracking.sh` | Log agent lifecycle | No agent tracking |
| Stop | `stop-validate-docs.sh` | Validate documentation | Incomplete docs allowed |
| Stop | `stop-hierarchy-update.sh` | Update parent timelines | Parent state stale |
| SessionEnd | `session-end-context-update.sh` | Context cleanup | Context leaks |

### 2. Hardcoded Path Dependencies in Hooks

**session-start-blackbox5.sh lines 211-214:**
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BB5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"
```

**subagent-tracking.sh lines 8-11:**
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BB5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"
COMM_DIR="$BB5_DIR/.autonomous/agents/communications"
```

### 3. Agent Type Detection Assumes Hook Behavior

**session-start-blackbox5.sh lines 12-67:**
```bash
# Method 1: Check run directory path
if [[ "$run_dir" == *"/planner/"* ]] || [[ "$cwd" == *"/planner/"* ]]; then
    echo "planner"
# Method 2: Check for agent-specific files
if [ -f "queue.yaml" ] || [ -f "loop-metadata-template.yaml" ]; then
    echo "planner"
```

**Problem:** File patterns (`queue.yaml`, `loop-metadata-template.yaml`) are BB5-specific.

### 4. RALF_RUN_DIR Environment Variable Dependency

**pre-tool-security.py lines 16-17:**
```python
cwd = os.getcwd()
run_dir = os.environ.get('RALF_RUN_DIR', cwd)
```

**subagent-tracking.sh lines 165-181:**
```bash
# Method 1: Check RALF_RUN_ID environment variable
if [ -n "${RALF_RUN_ID:-}" ]; then
    run_id="${RALF_RUN_ID}"
fi

# Method 2: Extract run_id from RALF_RUN_DIR
if [ -n "${RALF_RUN_DIR:-}" ]; then
    run_id=$(basename "${RALF_RUN_DIR}")
```

### 5. RALF Prompt Assumes Hook-Created Context

**ralf.md lines 41-55:**
```markdown
1. **Use Pre-Created Run** → `$RALF_RUN_DIR` is already created with template files
   (THOUGHTS.md, RESULTS.md, DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md)
```

**The run directory and templates are created by Claude Code hooks, not by RALF itself.**

### 6. Triggers Assume BB5-Specific Events

**timeline-maintenance.sh lines 36-75:**
```bash
case "$TOOL_NAME" in
    "Write"|"Edit")
        # Detect goal creation
        if echo "$FILE_PATH" | grep -qE "/goals/active/[^/]+/goal\.yaml$"; then
            GOAL_ID=$(basename "$(dirname "$FILE_PATH")")
            EVENT_TYPE="milestone"
```

**Assumes:** Goals stored in `/goals/active/GOAL-ID/goal.yaml`

**context-synchronization.sh lines 33-50:**
```bash
# If task completed, update parent goal progress
if echo "$file_path" | grep -qE "/tasks/active/[^/]+/task\.md$"; then
    for goal_dir in "$BB5_DIR"/goals/active/*; do
```

**Assumes:** Symlink-based hierarchy: `goals/active/GOAL/plans/PLAN -> plans/active/PLAN`

### 7. settings.json Hardcodes BB5 Paths

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "command": "bash /Users/shaansisodia/.blackbox5/.claude/hooks/session-start-blackbox5.sh"
          }
        ]
      }
    ]
  }
}
```

**Every hook path is an absolute path to BlackBox5.**

## What Happens If Hooks Aren't Configured

| Missing Hook | RALF Behavior | Impact |
|--------------|---------------|--------|
| SessionStart | Runs without context | No task awareness |
| PreToolUse (security) | No validation | Dangerous commands allowed |
| PreToolUse (validation) | No structure validation | Files written to wrong locations |
| PostToolUse (timeline) | Timeline not updated | Stale project state |
| PostToolUse (context) | No synchronization | State divergence |
| Subagent hooks | No tracking | Lost agent lifecycle |
| Stop (validate) | Docs not validated | Incomplete documentation |
| Stop (hierarchy) | Parent not updated | Stale parent state |
| SessionEnd | No cleanup | Context leaks |

## What Loop 1 Missed

Loop 1 focused on **configuration dependencies** but missed:

1. **Behavioral coupling**: RALF expects hooks to create `RALF_RUN_DIR` with templates
2. **Validation coupling**: RALF expects Stop hook to validate documentation
3. **Context coupling**: RALF expects SessionStart hooks to load agent context
4. **Security coupling**: RALF relies on PreToolUse hooks for security
5. **State synchronization**: RALF expects PostToolUse hooks to sync state
6. **Agent tracking**: RALF expects Subagent hooks to track lifecycle

## Decoupling Recommendations

### Immediate (High Priority)
1. **Make hooks optional** - Add `RALF_SKIP_HOOKS` environment variable
2. **Extract hook configuration** - Move to `2-engine/.autonomous/config/hooks.yaml`
3. **Remove hardcoded paths** - Use relative paths from `RALF_ENGINE_DIR`

### Short-term (Medium Priority)
4. **Create hook abstraction layer** - Define hook interface
5. **Make RALF self-initializing** - Create run directory if hooks don't
6. **Extract BB5-specific logic** - Move to `5-project-memory/blackbox5/hooks/`

### Long-term (Low Priority)
7. **Create hook plugin system** - Hooks register via manifest files
8. **Document hook contract** - Define what hooks must provide

## Summary

RALF's coupling to Claude Code hooks is **architectural**. The system assumes:
1. Hooks will create and initialize run directories
2. Hooks will validate documentation on stop
3. Hooks will enforce security on tool use
4. Hooks will synchronize state after tool use
5. Hooks will track agent lifecycle

**Without Claude Code hooks, RALF loses:**
- Security enforcement
- Documentation validation
- State synchronization
- Agent tracking
- Context initialization

This is a **fundamental architectural dependency** requiring significant refactoring.
