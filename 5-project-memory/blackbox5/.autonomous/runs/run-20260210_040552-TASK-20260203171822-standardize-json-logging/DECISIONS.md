# Run Decisions: TASK-20260203171822

## Decision 1: Include All BB5 Hooks, Not Just 3

**Context**: Task initially mentioned only 3 hooks (2 bash + 1 python), but inventory revealed 4 additional Python hooks.

**Decision**: Update all 7 BB5 hooks (3 originally done + 4 discovered).

**Rationale**:
- Incomplete hook inventory led to misunderstanding
- Standardizing all hooks is cleaner and more maintainable
- Follows "Do it right the first time" principle

## Decision 2: Use Shared JSON Logger Utility

**Context**: Several hooks had custom JSON logging code.

**Decision**: All hooks import `hooks.utils.json_logger.log_hook_data()` instead of inline logging.

**Rationale**:
- DRY principle - avoid duplicating logging code
- Consistent behavior across all hooks
- Easier to maintain and debug
- Centralized error handling

## Decision 3: Standardize Log Directory Location

**Context**: `pre-tool-security.py` used `~/.blackbox5/.logs/` while others used `logs/`.

**Decision**: All hooks use `logs/{hook_name}.json` in project root.

**Rationale**:
- Single source of truth for logs
- Consistent with documentation
- Easier for tools to find logs
- No dependency on HOME directory

## Decision 4: Minimal Changes to Hook Logic

**Context**: Some hooks had complex logic around logging.

**Decision**: Only add logging calls without modifying core hook functionality.

**Rationale**:
- Lower risk of introducing bugs
- Preserves existing behavior
- Logging is non-blocking
- Can add more logging later if needed

## Decision 5: Continue Using Existing Log Structure

**Context**: JSON logger appends to list: `[{timestamp, data}, ...]`.

**Decision**: Keep existing log structure, it's working well.

**Rationale**:
- Well-tested by original implementation
- Supports multiple entries per hook invocation
- Enables analytics and aggregation
- Matches mastery hooks pattern
