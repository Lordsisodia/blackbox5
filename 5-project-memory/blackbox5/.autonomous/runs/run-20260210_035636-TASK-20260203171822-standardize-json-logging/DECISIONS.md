# DECISIONS - TASK-20260203171822-standardize-json-logging

**Started:** 2026-02-10T03:56:36Z

## Decisions Made

### 1. Use Shared JSON Logger Utility

**Decision**: Create `hooks/utils/json_logger.py` instead of duplicating logging code.

**Rationale**: Even though BB5 only has 3 hooks, this follows best practices for extensibility. The mastery hooks have 13 hooks, and the pattern applies across the ecosystem.

**Impact**:
- Reduces code duplication
- Ensures consistency
- Makes future hook additions easier
- Provides utility functions for reading/writing logs

### 2. Bash Logging Pattern

**Decision**: Use inline `echo` statements for JSON logging in bash hooks.

**Rationale**:
- No external dependencies (Python calls from bash add overhead)
- Simpler to understand and maintain
- Matches the style used in mastery hooks' bash implementations

**Pattern**:
```bash
{
  echo "{"
  echo "  \"timestamp\": \"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\","
  echo "  \"hook\": \"my-hook.sh\","
  echo "  \"data\": ..."
  echo "}"
} >> "$LOG_FILE"
```

### 3. Log File Structure

**Decision**: Array of objects with timestamp and data.

**Format**:
```json
[
  {
    "timestamp": "2026-02-10T12:34:56.789012",
    "data": { ... }
  }
]
```

**Rationale**:
- Matches mastery pattern exactly
- Easy to append new entries
- Supports queries on individual entries
- Enables pagination if needed
- Allows querying "last N entries" or "entries after timestamp"

### 4. Error Handling Strategy

**Decision**: Gracefully handle JSON decode errors by starting fresh.

**Pattern**:
```python
try:
    log_data = json.load(f)
except (json.JSONDecodeError, ValueError):
    log_data = []
```

**Rationale**:
- Prevents crashes from corrupted logs
- Non-breaking error handling
- Ensures logs are always writable
- User can fix and restart

### 5. Log Directory Location

**Decision**: `logs/` in project root (same as mastery hooks).

**Rationale**:
- Consistent with mastery hooks
- Easy to access
- Standard convention for log files
- No subdirectories needed per hook

### 6. Log Rotation Strategy

**Decision**: Document strategy but defer implementation.

**Strategy** (documented in LOGGING.md):
- Size-based: 10 MB rotation
- Time-based: 30 days retention
- Combined: Rotate when either threshold is met

**Rationale**:
- Implementation can be added later as a standalone utility
- Documentation provides clear guidance
- Doesn't block hook standardization

## Trade-offs

| Decision | Trade-off | Mitigation |
|----------|-----------|------------|
| Shared utility for 3 hooks | Slight overhead of import | Minimal; Python imports are fast |
| Bash logging vs Python | Less flexible | Can convert to Python if needed |
| No rotation yet | Logs can grow large | Documented strategy; easy to implement |

## Dependencies

**External Dependencies**: None added. All solutions use standard library or shell built-ins.

**Internal Dependencies**:
- `json_logger.py` depends only on Python standard library
- Bash hooks use standard shell built-ins
