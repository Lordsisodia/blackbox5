# RALF Hook JSON Logging Schema

## Overview

All RALF hooks in BlackBox5 use a standardized JSON logging pattern to ensure consistent, structured logging across the system. This enables analytics, debugging, auditing, and log aggregation.

## Log Location

All logs are written to the `logs/` directory in the project root:

```
logs/
├── session-start-agent-teams.json
├── post-message-agent-teams.json
├── pre_tool_use.json
└── ...
```

## Log Format

Each hook log file contains an array of log entries:

```json
[
  {
    "timestamp": "2026-02-10T12:34:56.789012",
    "data": { /* hook-specific data */ }
  },
  {
    "timestamp": "2026-02-10T12:35:01.234567",
    "data": { /* next log entry */ }
  }
]
```

### Field Structure

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | ISO 8601 format timestamp (e.g., `2026-02-10T12:34:56.789012`) |
| `data` | object | The hook's input data |

## Helper Function

BB5 provides a shared utility for JSON logging: `hooks.utils.json_logger.log_hook_data()`

### Usage

```python
from hooks.utils.json_logger import log_hook_data
import json

def main():
    # Read JSON input from stdin
    input_data = json.load(sys.stdin)

    # Log the data
    log_hook_data("hook_name", input_data)

    # ... rest of hook logic
```

### Available Functions

| Function | Description |
|----------|-------------|
| `log_hook_data(hook_name, data)` | Append data to logs/{hook_name}.json |
| `read_hook_log(hook_name)` | Read existing log entries |
| `get_hook_log_file(hook_name)` | Get log file path |
| `get_total_log_entries(hook_name)` | Get number of log entries |
| `clear_hook_log(hook_name)` | Clear all log entries |
| `get_latest_log_entry(hook_name)` | Get most recent entry |

## Bash Hook Logging

Bash hooks use the following pattern for JSON logging:

```bash
#!/bin/bash
LOG_FILE="logs/my-hook.json"

mkdir -p "$(dirname "$LOG_FILE")"

{
  echo "{"
  echo "  \"timestamp\": \"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\","
  echo "  \"hook\": \"my-hook.sh\","
  echo "  \"data\": $(echo "$MY_DATA" | jq -c .)"
  echo "}"
} >> "$LOG_FILE"
```

## Log Rotation Strategy

BB5 recommends implementing log rotation to prevent log files from growing too large. Recommended policies:

### Retention Policy

| Policy | Threshold | Action |
|--------|-----------|--------|
| Size-based | 10 MB | Rotate to archive and create new log |
| Time-based | 30 days | Archive or delete old logs |
| Combined | 10 MB OR 30 days | Rotate when either threshold is reached |

### Rotation Example (Bash)

```bash
LOG_FILE="logs/my-hook.json"
MAX_SIZE=$((10 * 1024 * 1024))  # 10 MB
AGE_LIMIT=$((30 * 24 * 60 * 60))  # 30 days in seconds

# Check file size
if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null) -gt $MAX_SIZE ]; then
  mv "$LOG_FILE" "${LOG_FILE}.$(date +%Y%m%d_%H%M%S).archived"
fi

# Check file age
if [ -f "$LOG_FILE" ]; then
  file_age=$(($(date +%s) - $(stat -f%m "$LOG_FILE" 2>/dev/null)))
  if [ $file_age -gt $AGE_LIMIT ]; then
    mv "$LOG_FILE" "${LOG_FILE}.$(date +%Y%m%d_%H%M%S).expired"
  fi
fi
```

## Success Criteria

- [x] All hooks log to `logs/{hook_name}.json`
- [x] All hooks use consistent JSON structure
- [x] All hooks append to existing logs (don't overwrite)
- [ ] Log rotation strategy defined (see above)
- [x] Documentation updated with logging schema
- [x] Helper function created for reuse
- [x] All 2 bash hooks and 1 Python hook updated

## Migration Guide

### For Existing Hooks

1. Identify the hook's log file location
2. Replace existing logging with the standardized pattern
3. Test that logs are being written correctly
4. Update documentation if needed

### Example Migration (Bash)

**Before:**
```bash
echo "{
  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
  \"event\": \"my_event\"
}" >> "$OLD_LOG_FILE"
```

**After:**
```bash
LOG_FILE="logs/my-hook.json"
{
  echo "{"
  echo "  \"timestamp\": \"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\","
  echo "  \"hook\": \"my-hook.sh\","
  echo "  \"event\": \"my_event\""
  echo "}"
} >> "$LOG_FILE"
```

### Example Migration (Python)

**Before:**
```python
import json
from pathlib import Path

log_dir = Path.cwd() / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / 'my_hook.json'

if log_path.exists():
    with open(log_path, 'r') as f:
        log_data = json.load(f)
else:
    log_data = []

log_data.append(input_data)

with open(log_path, 'w') as f:
    json.dump(log_data, f, indent=2)
```

**After:**
```python
from hooks.utils.json_logger import log_hook_data
import json

def main():
    input_data = json.load(sys.stdin)
    log_hook_data("my_hook", input_data)
```

## References

- Analysis: `6-roadmap/_research/external/GitHub/Claude-Code/extracted/repos/RALF-HOOKS-ANALYSIS.md`
- Integration Plan: `5-project-memory/blackbox5/.autonomous/tasks/hooks-integration/HOOKS-INTEGRATION-PLAN.md`
- Mastery Hooks: `6-roadmap/_research/external/GitHub/Claude-Code/data/repos/claude-code-hooks-mastery/`
