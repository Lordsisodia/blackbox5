# THOUGHTS

## Initial Analysis

1. **Current State**: The BB5 project has no `session_start.py` hook - only a shell script for agent teams
2. **Source Reference**: The mastery repo (`claude-code-hooks-mastery`) has a comprehensive `session_start.py` that implements:
   - Git status (branch, uncommitted changes)
   - Context file loading
   - JSON logging to `logs/session_start.json`
   - Returns `additionalContext` to Claude

3. **Key Observation**: The mastery repo's implementation is nearly identical to what the task requires. I could either:
   a) Copy and adapt it with minor BB5-specific changes
   b) Integrate its functionality into a new BB5 implementation

I chose option (b) to maintain BB5-specific patterns and add proper documentation.

## Implementation Decisions

1. **File Location**: `.claude/hooks/session_start.py` (same pattern as other hooks)
2. **Hook Registration**: Added to `settings.json` with `"session_start"` key
3. **Context Files**: Loading priority order: `.claude/CONTEXT.md` > `.claude/TODO.md` > `TODO.md`
4. **JSON Logging**: Stores full input data with timestamp in `logs/session_start.json`
5. **Command-line Argument**: `--load-context` flag to conditionally load context (matches mastery pattern)

## Testing Plan

Due to the architecture of BB5, I cannot directly "test" the hook in the traditional sense. The hook will be invoked by the BB5 system during actual session starts/resumes.

Test scenarios:
1. Fresh session (source: "startup") - should load context
2. Resumed session (source: "resume") - should load context
3. Cleared session (source: "clear") - should load context

## Rationale

The hook pattern from mastery repo is solid and follows the same structure as other BB5 hooks. Key features:
- Graceful error handling (exits with 0 on errors)
- JSON input/output format
- Optional context loading via flags
- Git status integration
- Context file caching with length limits
