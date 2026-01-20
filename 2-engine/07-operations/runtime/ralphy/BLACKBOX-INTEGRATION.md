# Ralphy-Blackbox Integration Guide

## Overview

This integration ensures **Ralphy uses the Blackbox5 AgentMemory system** to track all agent activity with:
1. ✅ Goals and objectives
2. ✅ Task achievements
3. ✅ Code outputted
4. ✅ Timestamps and duration

## Problem Solved

**Before**: Ralphy only stored data in local `.ralphy/` directory, which was not integrated with the Blackbox system.

**After**: Ralphy now stores all session data in Project Memory alongside other agents, ensuring complete tracking of:
- What goals agents had
- What they were trying to achieve
- What code was outputted
- When all of this occurred

## Architecture

### Data Flow

```
User runs Ralphy
       ↓
ralphy-bb5-integrated.sh
       ↓
1. Starts Blackbox session (via blackbox_integration.py)
   - Creates session record
   - Stores in .blackbox5/5-project-memory/siso-internal/operations/ralphy/
   - Tracks: agent_id, task, engine, timestamp
       ↓
2. Executes Ralphy task
   - Runs ralphy.sh
   - Creates code files
   - Makes git commits
       ↓
3. Ends Blackbox session
   - Records success/failure
   - Lists files created
   - Captures git commit hash
   - Calculates duration
       ↓
4. Archives to Project Memory
   - history/sessions/ralphy/sessions.json
   - history/sessions/ralphy/{session_id}/session.json
   - active/session.json (cleared after completion)
```

## Project Memory Structure

```
.blackbox5/5-project-memory/siso-internal/operations/ralphy/
├── active/
│   └── session.json              # Currently running session
├── history/
│   └── sessions/
│       └── ralphy/
│           ├── sessions.json     # All session records
│           ├── ralphy_20260119_120000_abc123/  # Individual sessions
│           │   ├── session.json
│           │   ├── progress.jsonl
│           │   └── files.json
│           ├── insights.json     # Learned patterns
│           ├── patterns.json     # Discovered patterns
│           └── metrics.json      # Performance metrics
└── .active_session               # Temporary session ID file
```

## Session Data Structure

### Active Session (`active/session.json`)

```json
{
  "agent_id": "ralphy",
  "agent_type": "autonomous_coding",
  "session_start": "2026-01-19T12:00:00Z",
  "task": "Create calculator.py with arithmetic functions",
  "status": "active",
  "session_id": "ralphy_20260119_120000_abc123",
  "context": {
    "project": "/path/to/project",
    "engine": "claude",
    "prd_file": "PRD.md",
    "blackbox_integration": true
  }
}
```

### Session Record (`history/sessions/ralphy/sessions.json`)

```json
[
  {
    "session_id": "ralphy_20260119_120000_abc123",
    "timestamp": "2026-01-19T12:00:00Z",
    "task": "Create calculator.py with arithmetic functions",
    "result": "Task completed successfully. Created 2 file(s). Commit: abc123",
    "metadata": {
      "engine": "claude",
      "files_created": ["calculator.py", "test_calculator.py"],
      "git_commit": "abc123",
      "duration_seconds": 45.2
    },
    "success": true,
    "duration_seconds": 45.2
  }
]
```

## Usage

### Method 1: Integrated Wrapper (Recommended)

```bash
# Use the integrated wrapper
.blackbox5/2-engine/07-operations/runtime/ralphy-bb5-integrated.sh \
  --claude \
  --prd PRD.md \
  "Create a Python class for user authentication"
```

**Benefits**:
- ✅ Automatic session tracking
- ✅ Progress logging
- ✅ File change detection
- ✅ Git commit capture
- ✅ Duration calculation

### Method 2: Python Integration

```python
from blackbox5.engine.operations.runtime.ralphy.blackbox_integration import create_bridge

# Create bridge
bridge = create_bridge()

# Start session
session_id = bridge.start_session(
    task="Create calculator.py",
    engine="claude",
    metadata={"project": "my-project"}
)

# Log progress
bridge.log_progress("Starting task...", "info")
bridge.log_progress("Creating files...", "milestone")

# End session
summary = bridge.end_session(
    success=True,
    result="Task completed",
    files_created=["calculator.py", "test_calculator.py"],
    git_commit="abc123"
)

print(f"Duration: {summary['duration_seconds']} seconds")
```

### Method 3: Direct Ralphy (No Tracking)

```bash
# Use original ralphy.sh (no Blackbox tracking)
.blackbox5/2-engine/07-operations/runtime/ralphy/ralphy.sh \
  --claude \
  --prd PRD.md \
  "Create a Python calculator"
```

**Note**: This will use `RALPHY_DIR` but won't track sessions in AgentMemory.

## Integration Points

### 1. Session Start

When Ralphy starts, the wrapper:
1. Creates `RalphyBlackboxBridge` instance
2. Calls `bridge.start_session()` with task, engine, PRD
3. Stores active session in `active/session.json`
4. Saves session ID to `.active_session` file

### 2. Progress Logging (Optional)

During execution, you can log progress:
```python
bridge.log_progress("Analyzing requirements...", "info")
bridge.log_progress("Writing code...", "milestone")
bridge.log_progress("Testing...", "info")
```

This creates `sessions/{session_id}_progress.jsonl` with timestamped entries.

### 3. Insights Learning (Optional)

After completion, add learned insights:
```python
bridge.add_insight(
    content="Use pytest for test discovery",
    category="pattern",
    confidence=0.9
)
```

### 4. Session End

When Ralphy completes, the wrapper:
1. Detects files created (modified in last minute)
2. Captures git commit hash
3. Calculates duration
4. Calls `bridge.end_session()` with results
5. Archives to `history/sessions/ralphy/`
6. Clears `active/session.json`

## AgentMemory Integration

The bridge uses `AgentMemory` class if available:

```python
from blackbox5.engine.knowledge.memory.AgentMemory import AgentMemory

# Initialize with Project Memory path
memory = AgentMemory(
    agent_id="ralphy",
    memory_base_path=Path("blackbox5/5-project-memory/siso-internal/operations")
)

# Add session
memory.add_session(
    task="Create calculator.py",
    result="Task completed successfully",
    success=True,
    duration_seconds=45.2,
    metadata={
        "engine": "claude",
        "files_created": ["calculator.py"],
        "git_commit": "abc123"
    }
)

# Add insight
memory.add_insight(
    content="Use type hints for better code clarity",
    category="pattern",
    confidence=0.95,
    source_session="ralphy_20260119_120000_abc123"
)
```

## Testing the Integration

### Test 1: Simple Task

```bash
cd /tmp/ralphy-test-3
git init
cat > PRD.md <<EOF
# Task: Create Greeter Class

Create a Python class with hello, goodbye, and greet methods.
EOF

# Run with integrated wrapper
.blackbox5/2-engine/07-operations/runtime/ralphy-bb5-integrated.sh \
  --claude \
  --prd PRD.md \
  "Create greeter.py"

# Check results
echo "=== Created Files ==="
ls -la

echo "=== Git Commits ==="
git log --oneline

echo "=== Project Memory ==="
ls -la .blackbox5/5-project-memory/siso-internal/operations/ralphy/

echo "=== Session Record ==="
cat .blackbox5/5-project-memory/siso-internal/operations/ralphy/history/sessions/ralphy/sessions.json
```

### Test 2: Python Integration

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, "blackbox5")

from engine.operations.runtime.ralphy.blackbox_integration import create_bridge

# Test basic session
bridge = create_bridge()
session_id = bridge.start_session(
    task="Test integration",
    engine="claude"
)

print(f"Session: {session_id}")

bridge.log_progress("Step 1 complete", "info")
bridge.log_progress("Step 2 complete", "milestone")

summary = bridge.end_session(
    success=True,
    result="Test completed",
    files_created=["test.py"]
)

print("Summary:")
print(summary)
```

## Comparison: Before vs After

### Before (Local `.ralphy/` only)

```
/tmp/ralphy-test/
├── .ralphy/
│   ├── progress.txt        # Progress log
│   └── config.yaml         # Config
├── calculator.py           # Created file
└── test_calculator.py      # Created file

Git: abc123 "Add basic calculator"

**Problem**: No integration with Blackbox, no agent tracking
```

### After (Full Blackbox Integration)

```
.blackbox5/5-project-memory/siso-internal/operations/ralphy/
├── active/
│   └── session.json          # Active session (while running)
├── history/
│   └── sessions/
│       └── ralphy/
│           ├── sessions.json           # All sessions
│           │   [0] session_id, timestamp, task, result, success
│           ├── ralphy_20260119_120000/  # Individual session
│           │   ├── session.json
│           │   ├── progress.jsonl       # Progress logs
│           │   └── files.json           # Created files
│           ├── insights.json           # Learned patterns
│           └── metrics.json            # Performance metrics

/tmp/ralphy-test/
├── calculator.py               # Created file
└── test_calculator.py          # Created file

Git: abc123 "Add basic calculator"

**Benefits**: Full integration, complete tracking, agent insights
```

## Troubleshooting

### Issue: Sessions not being tracked

**Check**:
1. Is `ralphy-bb5-integrated.sh` executable?
2. Is Python 3 available?
3. Is `blackbox_integration.py` in the correct location?
4. Check stderr output for `[Blackbox]` messages

**Debug**:
```bash
# Run with verbose output
bash -x .blackbox5/2-engine/07-operations/runtime/ralphy-bb5-integrated.sh \
  --claude --prd PRD.md "Task"
```

### Issue: AgentMemory not found

**Solution**: The integration works without AgentMemory, but sessions won't be stored in the centralized memory system. Check the import path in `blackbox_integration.py`.

### Issue: Files not detected

**Cause**: File detection uses modification time (last 1 minute).

**Solution**: If files were created earlier, manually specify them:
```python
summary = bridge.end_session(
    success=True,
    result="Task completed",
    files_created=["file1.py", "file2.py"]  # Manually specify
)
```

## Future Enhancements

1. **Real-time progress streaming**: Stream progress to Blackbox during execution
2. **Insight extraction**: Automatically extract insights from completed tasks
3. **Pattern recognition**: Identify patterns across multiple Ralphy sessions
4. **Cost tracking**: Track API costs per session
5. **Multi-agent coordination**: Share insights between Ralphy and other agents

## Summary

✅ **Integration Complete**: Ralphy now uses the Blackbox AgentMemory system

✅ **Data Tracked**:
- Goals and objectives (task descriptions)
- Task achievements (success/failure, results)
- Code outputted (files created, git commits)
- Timestamps and duration (start, end, duration)

✅ **Storage Location**: `.blackbox5/5-project-memory/siso-internal/operations/ralphy/`

✅ **Compatibility**: Works with existing Ralphy workflow, transparent to users

---

## MCP Configuration Issue & Fix

### Problem: Ralphy hangs at "Thinking" state

**Symptom**: When running Ralphy, it gets stuck at "Thinking" or "Logging" state indefinitely.

**Root Cause**: Claude Code CLI is configured with multiple MCP servers (e.g., playwright, chrome-devtools, browser-mcp) that take a very long time to initialize or may timeout.

When Ralphy calls Claude Code, it waits for:
1. All MCP servers to initialize
2. Each server to be ready
3. The handshake to complete

With 12+ MCP servers, this can take 2+ minutes or hang indefinitely.

### Solution: Tiered MCP Profile System

Instead of a single config, use **different MCP profiles for different task types**. The Black Box can determine which profile to use based on the task requirements.

**Included Tool**: `ralphy-mcp-profiles.sh` manages MCP profiles automatically.

#### Setup (One-time)

```bash
# Initialize the profile system
./blackbox5/2-engine/07-operations/runtime/ralphy/ralphy-mcp-profiles.sh init
```

This creates profiles in `~/.claude-profiles/`:
- **minimal**: No MCP servers (fastest, ~1s startup)
- **filesystem**: Filesystem access only (~2s startup)
- **standard**: Common MCPs (filesystem, fetch, search, ~5s startup)
- **data**: Data & docs MCPs (filesystem, fetch, context7, wikipedia, ~10s startup)
- **automation**: Browser automation (filesystem, playwright, chrome-devtools, ~15s startup)
- **full**: All MCPs (slowest, ~30s+ startup)

#### Usage Methods

**Method 1: Manual Profile Selection**

```bash
# List available profiles
./ralphy-mcp-profiles.sh list

# Switch to a profile
./ralphy-mcp-profiles.sh use automation

# Run Ralphy with active profile
eval $(./ralphy-mcp-profiles.sh export)
ralphy.sh --prd PRD.md
```

**Method 2: Auto-Detection from Task**

```bash
# Auto-detect best profile for a task
./ralphy-mcp-profiles.sh detect "Create a web scraper using playwright"
# Output: Recommended profile: automation

./ralphy-mcp-profiles.sh detect "Create a Python class for data validation"
# Output: Recommended profile: minimal
```

**Method 3: Integration with Ralphy**

```bash
# One-liner with specific profile
CLAUDE_CONFIG_DIR=~/.claude-profiles/minimal ralphy.sh --prd PRD.md

# Or use the export command
eval $(./ralphy-mcp-profiles.sh export minimal)
ralphy.sh --prd PRD.md
```

#### Profile Selection Logic

The `ralphy-mcp-profiles.sh detect` command uses keyword matching:

| Task Keywords | Recommended Profile | Why |
|--------------|-------------------|-----|
| browser, scrape, screenshot, web, chrome, playwright, headless | **automation** | Needs browser tools |
| search, documentation, docs, wikipedia, research, context, reference | **data** | Needs data lookup |
| fetch, http, api, url, download | **standard** | Needs web requests |
| (none of the above) | **minimal** | Pure coding, no external tools needed |

#### Performance Comparison

| Profile | MCP Servers | Startup Time | Best For |
|---------|-------------|--------------|----------|
| minimal | 0 | ~1 second | Pure coding tasks |
| filesystem | 1 | ~2 seconds | File operations |
| standard | 3 | ~5 seconds | APIs + web |
| data | 4 | ~10 seconds | Research + docs |
| automation | 3 | ~15 seconds | Browser automation |
| full | 8+ | ~30+ seconds | Everything (slowest) |

#### Integration with Black Box

The Black Box can automatically select the appropriate profile:

```python
# In your Black Box task runner
import subprocess
import os

def run_ralphy_with_profile(task_description, prd_file):
    # Detect appropriate profile
    result = subprocess.run(
        ["./ralphy-mcp-profiles.sh", "detect", task_description],
        capture_output=True, text=True
    )

    # Extract profile from output
    profile = "minimal"  # fallback
    for line in result.stdout.split("\n"):
        if "Recommended profile:" in line:
            profile = line.split()[-1]
            break

    # Set config dir and run Ralphy
    config_dir = f"{os.path.expanduser('~')}/.claude-profiles/{profile}"
    env = os.environ.copy()
    env["CLAUDE_CONFIG_DIR"] = config_dir

    subprocess.run(["ralphy.sh", "--prd", prd_file], env=env)
```

### Summary

- **Problem**: MCP server initialization causes Ralphy to hang
- **Solution**: Tiered profile system with task-based selection
- **Tool**: `ralphy-mcp-profiles.sh` manages profiles automatically
- **Benefit**: Fast startup for simple tasks, MCPs available when needed
- **Integration**: Black Box can auto-select profiles based on task analysis
