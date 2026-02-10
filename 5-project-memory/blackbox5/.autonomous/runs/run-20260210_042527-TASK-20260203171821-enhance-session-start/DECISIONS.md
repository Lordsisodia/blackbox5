# DECISIONS

## Decision 1: Create New SessionStart Hook File

**Decision**: Create `.claude/hooks/session_start.py` from scratch rather than copying the mastery repo's implementation.

**Rationale**:
- Maintain BB5-specific patterns and conventions
- Add proper BB5 documentation
- Reduce copy-paste dependencies on external repo
- Allows for BB5-specific optimizations (like using the existing `utils/json_logger.py`)

## Decision 2: Add Hook to settings.json

**Decision**: Added `"session_start": {"enabled": true, "path": ".claude/hooks/session_start.py"}` to settings.json.

**Rationale**:
- Matches the pattern of other BB5 hooks (pre_tool_use, subagent_start, etc.)
- Enables the hook system to discover and invoke it automatically
- Minimal change to existing configuration

## Decision 3: Context File Loading Priority

**Decision**: Load context files in priority order: `.claude/CONTEXT.md` > `.claude/TODO.md` > `TODO.md`.

**Rationale**:
- `.claude/CONTEXT.md` is the standard location for project context in the BB5 ecosystem
- `.claude/TODO.md` provides more granular task tracking
- `TODO.md` in root is the traditional location for project todos

## Decision 4: JSON Logging Structure

**Decision**: Store complete input data with timestamp in `logs/session_start.json` as a list of entries.

**Rationale**:
- Maintains chronological ordering of session starts
- Makes debugging easier (can see full input each time)
- Simple to implement and query later
- Matches pattern from mastery repo

## Decision 5: Graceful Error Handling

**Decision**: Catch all exceptions and exit with code 0 rather than raising errors.

**Rationale**:
- Hooks should never crash the Claude Code session
- Errors should be silent but logged for debugging
- Matches pattern from other BB5 hooks

## Decision 6: --load-context Flag

**Decision**: Include `--load-context` command-line flag to conditionally load context.

**Rationale**:
- Allows selective loading (e.g., during startup vs. for testing)
- Matches the pattern from mastery repo
- Provides flexibility for future customizations
