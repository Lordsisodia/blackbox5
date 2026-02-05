# Hook Environment Variables Guide

**Date:** 2026-02-06
**Purpose:** Comprehensive guide on environment variables for BB5 hooks
**Research:** Claude Code docs, BB5 hooks, ralph-loop, juno-code, SWE-agent

---

## Available Environment Variables

### Built-in Claude Code Variables

| Variable | Availability | Purpose | Example |
|----------|--------------|---------|---------|
| `CLAUDE_PROJECT_DIR` | All hooks | Project root path | `/Users/shaansisodia/.blackbox5` |
| `CLAUDE_PLUGIN_ROOT` | Plugin hooks | Plugin root directory | `/path/to/plugin` |
| `CLAUDE_ENV_FILE` | **SessionStart only** | File to persist env vars | `/tmp/claude-env-xxx` |
| `CLAUDE_CODE_REMOTE` | All hooks | "true" if remote web env | `true` or unset |

### BB5/RALF Custom Variables

| Variable | Set By | Purpose | Example |
|----------|--------|---------|---------|
| `RALF_RUN_DIR` | SessionStart hook | Current run directory | `/Users/.../runs/planner/run-20260206-011248` |
| `RALF_RUN_ID` | SessionStart hook | Run identifier | `run-20260206-011248` |
| `RALF_AGENT_TYPE` | SessionStart hook | Agent type | `planner`, `executor`, `architect` |
| `RALF_PROJECT_ROOT` | SessionStart hook | BB5 root path | `/Users/shaansisodia/.blackbox5` |
| `BB5_PROJECT` | SessionStart hook | Current project | `blackbox5`, `siso-internal` |

---

## CLAUDE_ENV_FILE - The Key to Persistence

### What It Is

`CLAUDE_ENV_FILE` is a file path provided **only to SessionStart hooks**. Any `export` statements written to this file are sourced before every subsequent Bash command during the session.

### How It Works

```
1. Claude Code creates temp file
2. Sets CLAUDE_ENV_FILE to that path
3. SessionStart hook writes export statements
4. Before each Bash command, Claude sources the file
5. Variables become available in Bash environment
```

### Critical Limitations

- **Only SessionStart hooks can use it**
- **Must use append (`>>`) not overwrite (`>`)**
- **Only affects Bash commands, not other hooks**
- **Persists for entire session**

### Example Usage

```bash
#!/bin/bash
# SessionStart hook

if [ -n "$CLAUDE_ENV_FILE" ]; then
    # Append exports (don't overwrite other hooks' vars)
    echo 'export RALF_RUN_DIR=/path/to/run' >> "$CLAUDE_ENV_FILE"
    echo 'export RALF_RUN_ID=run-20260206-011248' >> "$CLAUDE_ENV_FILE"
    echo 'export BB5_PROJECT=blackbox5' >> "$CLAUDE_ENV_FILE"
    echo 'export DEBUG_MODE=true' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

### Result

After the SessionStart hook runs, every Bash command in the session has access to:
- `$RALF_RUN_DIR`
- `$RALF_RUN_ID`
- `$BB5_PROJECT`
- `$DEBUG_MODE`

---

## Setting Environment Variables (SessionStart Only)

### Pattern 1: Simple Exports

```bash
#!/bin/bash
# In SessionStart hook

RUN_DIR="/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/runs/planner/run-20260206-011248"
RUN_ID="run-20260206-011248"
PROJECT="blackbox5"
AGENT_TYPE="planner"

# Export for current session (this hook only)
export RALF_RUN_DIR="$RUN_DIR"
export RALF_RUN_ID="$RUN_ID"
export BB5_PROJECT="$PROJECT"
export BB5_AGENT_TYPE="$AGENT_TYPE"

# Persist for all Bash commands in session
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "export RALF_RUN_DIR=$RUN_DIR" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_RUN_ID=$RUN_ID" >> "$CLAUDE_ENV_FILE"
    echo "export BB5_PROJECT=$PROJECT" >> "$CLAUDE_ENV_FILE"
    echo "export BB5_AGENT_TYPE=$AGENT_TYPE" >> "$CLAUDE_ENV_FILE"
fi
```

### Pattern 2: Capture Environment Changes

```bash
#!/bin/bash
# Capture all env changes after setup

# Record environment before
ENV_BEFORE=$(export -p | sort)

# Run setup commands that modify environment
source ~/.nvm/nvm.sh
nvm use 20
export NODE_ENV=production

# Record environment after
ENV_AFTER=$(export -p | sort)

# Write only new/changed variables to CLAUDE_ENV_FILE
if [ -n "$CLAUDE_ENV_FILE" ]; then
    comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi
```

### Pattern 3: Conditional Exports

```bash
#!/bin/bash
# Only set variables if they don't exist

if [ -n "$CLAUDE_ENV_FILE" ]; then
    # Check if already set
    if ! grep -q "RALF_RUN_DIR" "$CLAUDE_ENV_FILE" 2>/dev/null; then
        echo "export RALF_RUN_DIR=$RUN_DIR" >> "$CLAUDE_ENV_FILE"
    fi

    if ! grep -q "BB5_PROJECT" "$CLAUDE_ENV_FILE" 2>/dev/null; then
        echo "export BB5_PROJECT=$PROJECT" >> "$CLAUDE_ENV_FILE"
    fi
fi
```

---

## Using Environment Variables (All Hooks)

### Pattern 1: With Fallback

```bash
#!/bin/bash
# Any hook can READ env vars, but only SessionStart can SET them

# Use the variable if set, otherwise use default
RUN_DIR="${RALF_RUN_DIR:-$(pwd)}"
PROJECT="${BB5_PROJECT:-blackbox5}"
AGENT_TYPE="${BB5_AGENT_TYPE:-unknown}"

# Or detect from filesystem if not set
if [ -z "$PROJECT" ]; then
    PROJECT=$(detect_current_project)
fi
```

### Pattern 2: File-Based Fallback

```bash
#!/bin/bash
# SubagentStop hook - can't use CLAUDE_ENV_FILE

# Try environment variable first
if [ -n "${RALF_RUN_ID:-}" ]; then
    RUN_ID="$RALF_RUN_ID"
# Try to extract from RUN_DIR
elif [ -n "${RALF_RUN_DIR:-}" ]; then
    RUN_ID=$(basename "$RALF_RUN_DIR")
# Load from persisted context file
elif [ -f ".agent-context" ]; then
    RUN_ID=$(grep "run_id:" .agent-context | cut -d':' -f2 | tr -d ' ')
else
    RUN_ID="unknown"
fi
```

### Pattern 3: Python Hook Using Environment

```python
#!/usr/bin/env python3
# pre-tool-security.py

import os
from pathlib import Path

def get_run_directory():
    """Get run directory from env or fallback."""
    # Try environment variable
    run_dir = os.environ.get('RALF_RUN_DIR')
    if run_dir:
        return Path(run_dir)

    # Fallback to current working directory
    return Path.cwd()

def get_project_name():
    """Get project name from env or detect."""
    # Try environment variable
    project = os.environ.get('BB5_PROJECT')
    if project:
        return project

    # Detect from filesystem
    cwd = Path.cwd()
    if '5-project-memory' in str(cwd):
        parts = str(cwd).split('5-project-memory/')
        if len(parts) > 1:
            return parts[1].split('/')[0]

    return 'blackbox5'  # Default

# Use in hook
run_dir = get_run_directory()
project = get_project_name()
```

---

## Passing Data Between Hooks

### Method 1: File-Based Persistence (Recommended)

```bash
# SessionStart hook writes context
CONTEXT_FILE="$BB5_DIR/.agent-context"

cat > "$CONTEXT_FILE" << EOF
project: "$PROJECT"
agent_type: "$AGENT_TYPE"
run_id: "$RUN_ID"
run_dir: "$RUN_DIR"
timestamp: "$(date -Iseconds)"
EOF

# SubagentStop hook reads context
if [ -f "$CONTEXT_FILE" ]; then
    PROJECT=$(grep "project:" "$CONTEXT_FILE" | cut -d':' -f2 | tr -d ' "')
    AGENT_TYPE=$(grep "agent_type:" "$CONTEXT_FILE" | cut -d':' -f2 | tr -d ' "')
fi
```

### Method 2: Metadata Files

```bash
# Save metadata in run directory
METADATA_FILE="$RUN_DIR/.ralf-metadata"

cat > "$METADATA_FILE" << EOF
run:
  id: "$RUN_ID"
  timestamp: "$(date -Iseconds)"
  project: "$PROJECT"
  agent_type: "$AGENT_TYPE"
  status: initialized
EOF

# Other hooks read metadata
if [ -f "$METADATA_FILE" ]; then
    # Parse YAML or use simple grep
    RUN_ID=$(grep "id:" "$METADATA_FILE" | head -1 | cut -d':' -f2 | tr -d ' "')
fi
```

### Method 3: JSON Log Files

```python
# Python hook writing to shared log
import json
from pathlib import Path

def log_event(event_type, data):
    log_dir = Path('.logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'hook-events.jsonl'

    event = {
        'type': event_type,
        'timestamp': datetime.now().isoformat(),
        'data': data
    }

    with open(log_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

# Use in hook
log_event('session_start', {
    'project': project,
    'agent_type': agent_type,
    'run_id': run_id
})
```

---

## Best Practices

### DO

1. **Use self-discovery as primary method**:
   ```bash
   # Good: Detect from filesystem
   detect_project() {
       local cwd="$(pwd)"
       if [[ "$cwd" == *"5-project-memory/blackbox5"* ]]; then
           echo "blackbox5"
       fi
   }
   ```

2. **Use environment variables as optimization**:
   ```bash
   # Good: Use env var if available, fallback to detection
   PROJECT="${BB5_PROJECT:-$(detect_project)}"
   ```

3. **Always check CLAUDE_ENV_FILE exists before writing**:
   ```bash
   if [ -n "$CLAUDE_ENV_FILE" ]; then
       echo 'export VAR=value' >> "$CLAUDE_ENV_FILE"
   fi
   ```

4. **Use append (`>>`) not overwrite (`>`)**:
   ```bash
   # Good: Preserves other hooks' variables
   echo 'export VAR=value' >> "$CLAUDE_ENV_FILE"

   # Bad: Deletes other hooks' variables
   echo 'export VAR=value' > "$CLAUDE_ENV_FILE"
   ```

5. **Fail silently**:
   ```bash
   # Good: Never break user experience
   main_logic() || true
   exit 0
   ```

6. **Use absolute paths**:
   ```bash
   # Good: Full path
   "$CLAUDE_PROJECT_DIR"/.claude/hooks/script.sh

   # Bad: Relative path
   .claude/hooks/script.sh
   ```

### DON'T

1. **Don't rely on environment variables for critical logic**:
   ```bash
   # Bad: Fails if env var not set
   cd "$RALF_RUN_DIR"  # Could fail!

   # Good: With fallback
   cd "${RALF_RUN_DIR:-$(pwd)}"
   ```

2. **Don't write to CLAUDE_ENV_FILE from non-SessionStart hooks**:
   ```bash
   # This won't work in PreToolUse, Stop, etc.
   echo 'export VAR=value' >> "$CLAUDE_ENV_FILE"  # No effect!
   ```

3. **Don't assume environment variables persist between sessions**:
   ```bash
   # Each session is fresh - only CLAUDE_ENV_FILE persists within session
   ```

4. **Don't use relative paths**:
   ```bash
   # Bad: Unpredictable working directory
   cat .agent-context

   # Good: Absolute path
   cat "$BB5_DIR/.agent-context"
   ```

---

## Hook Type Reference

| Hook Event | CLAUDE_ENV_FILE | Can Read Env | Can Set Env | Can Block |
|------------|-----------------|--------------|-------------|-----------|
| **SessionStart** | ✅ Yes | ✅ Yes | ✅ Yes (via file) | ❌ No |
| UserPromptSubmit | ❌ No | ✅ Yes | ❌ No | ✅ Yes (exit 2) |
| PreToolUse | ❌ No | ✅ Yes | ❌ No | ✅ Yes (exit 2) |
| PostToolUse | ❌ No | ✅ Yes | ❌ No | ❌ No |
| SubagentStart | ❌ No | ✅ Yes | ❌ No | ❌ No |
| SubagentStop | ❌ No | ✅ Yes | ❌ No | ✅ Yes (exit 2) |
| Stop | ❌ No | ✅ Yes | ❌ No | ✅ Yes (exit 2) |
| SessionEnd | ❌ No | ✅ Yes | ❌ No | ❌ No |

---

## BB5 SessionStart Hook: Environment Variable Pattern

```bash
#!/bin/bash
# BB5 SessionStart Hook - Environment Variable Pattern

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BB5_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# =============================================================================
# STEP 1: DETECT PROJECT (Self-Discovery)
# =============================================================================

detect_project() {
    local cwd="$(pwd)"

    # Check working directory path
    if [[ "$cwd" == *"5-project-memory/blackbox5"* ]]; then
        echo "blackbox5"
        return
    elif [[ "$cwd" == *"5-project-memory/siso-internal"* ]]; then
        echo "siso-internal"
        return
    fi

    # Check for .bb5-project file
    if [ -f ".bb5-project" ]; then
        cat ".bb5-project"
        return
    fi

    # Default
    echo "blackbox5"
}

# Use env var if set, otherwise detect
PROJECT="${BB5_PROJECT:-$(detect_project)}"

# =============================================================================
# STEP 2: DETECT AGENT TYPE (Self-Discovery)
# =============================================================================

detect_agent_type() {
    local cwd="$(pwd)"

    # Check path patterns
    if [[ "$cwd" == *"/planner/"* ]]; then
        echo "planner"
    elif [[ "$cwd" == *"/executor/"* ]]; then
        echo "executor"
    elif [[ "$cwd" == *"/architect/"* ]]; then
        echo "architect"
    else
        echo "developer"
    fi
}

# Use env var if set, otherwise detect
AGENT_TYPE="${BB5_AGENT_TYPE:-$(detect_agent_type)}"

# =============================================================================
# STEP 3: CREATE RUN DIRECTORY
# =============================================================================

RUN_TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="run-$RUN_TIMESTAMP"
RUN_DIR="$BB5_ROOT/5-project-memory/$PROJECT/runs/$AGENT_TYPE/$RUN_ID"

mkdir -p "$RUN_DIR"

# =============================================================================
# STEP 4: EXPORT FOR CURRENT SESSION
# =============================================================================

export BB5_PROJECT="$PROJECT"
export BB5_AGENT_TYPE="$AGENT_TYPE"
export RALF_RUN_DIR="$RUN_DIR"
export RALF_RUN_ID="$RUN_ID"

# =============================================================================
# STEP 5: PERSIST FOR BASH COMMANDS (SessionStart Only!)
# =============================================================================

if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "# BB5 SessionStart Environment Variables" >> "$CLAUDE_ENV_FILE"
    echo "export BB5_PROJECT=$PROJECT" >> "$CLAUDE_ENV_FILE"
    echo "export BB5_AGENT_TYPE=$AGENT_TYPE" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_RUN_DIR=$RUN_DIR" >> "$CLAUDE_ENV_FILE"
    echo "export RALF_RUN_ID=$RUN_ID" >> "$CLAUDE_ENV_FILE"
fi

# =============================================================================
# STEP 6: CREATE CONTEXT FILES
# =============================================================================

# Create THOUGHTS.md, RESULTS.md, etc.
# ... (see full implementation)

# =============================================================================
# STEP 7: RETURN JSON OUTPUT
# =============================================================================

cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Project: $PROJECT | Agent: $AGENT_TYPE | Run: $RUN_ID",
    "project": "$PROJECT",
    "agentType": "$AGENT_TYPE",
    "runDir": "$RUN_DIR",
    "runId": "$RUN_ID"
  }
}
EOF
```

---

## Summary

### Key Points

1. **Only SessionStart hooks can set environment variables** using `CLAUDE_ENV_FILE`
2. **All hooks can read environment variables** set by SessionStart
3. **Use self-discovery as primary method** - env vars are optimization
4. **Use file-based persistence** for passing data between non-SessionStart hooks
5. **Always use fallbacks** - never assume env vars are set
6. **Fail silently** - hooks should never break the user experience

### For BB5 SessionStart Hook

The hook must:
1. Detect project (with `BB5_PROJECT` env var as override)
2. Detect agent type (with `BB5_AGENT_TYPE` env var as override)
3. Create run directory
4. **Export variables for current session**
5. **Write to `CLAUDE_ENV_FILE` for persistence**
6. Create context files
7. Return JSON output

This ensures all subsequent Bash commands have access to:
- `$BB5_PROJECT` - Current project name
- `$BB5_AGENT_TYPE` - Agent type
- `$RALF_RUN_DIR` - Run directory path
- `$RALF_RUN_ID` - Run identifier
