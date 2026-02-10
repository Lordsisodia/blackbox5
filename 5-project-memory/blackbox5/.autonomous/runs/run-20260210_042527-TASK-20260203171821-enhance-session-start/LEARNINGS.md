# LEARNINGS

## Learning 1: BB5 Hook Architecture

BB5 hooks run as Python scripts that:
1. Read JSON from stdin (input data)
2. Optionally process it
3. Write JSON to stdout (output data)
4. Exit with code 0 on success

The hook system in BB5 automatically:
- Invokes hooks at appropriate times
- Passes session metadata as input
- Captures and returns hook outputs to Claude

## Learning 2: Session Source Values

The `source` field in SessionStart input can be:
- `"startup"` - Fresh session start
- `"resume"` - Resuming a previous session
- `"clear"` - Starting with a cleared context

Each source should be handled appropriately for context loading.

## Learning 3: Git Status Detection

Using `git status --porcelain` is better than `git status` for counting changes:
- Returns machine-readable format (one file per line)
- Much faster than full status output
- Simple to count lines for uncommitted changes

## Learning 4: Context File Caching

Context files are cached on disk. For efficiency:
- Limit content to 1000 characters per file
- Skip files that are empty after stripping whitespace
- Only include context if files actually exist

## Learning 5: Hook Invocation

Unlike mastery repo's optional TTS announcement, BB5's architecture doesn't require explicit announcements. The hook's primary value is returning `additionalContext` to Claude.

## Learning 6: SessionStart Input Format

Input includes:
- `session_id` - Unique identifier for the session
- `source` - The source of the session (startup/resume/clear)
- Additional metadata (timestamp, etc. - depends on Claude Code version)

## Learning 7: Settings.json Pattern

All BB5 hooks follow the same registration pattern:
```json
{
  "hooks": {
    "hook_name": {
      "enabled": true,
      "path": ".claude/hooks/hook_file.py"
    }
  }
}
```

Adding a new hook just requires adding one entry to the hooks object.

## Learning 8: JSON Logging Best Practices

For session logging:
- Store data as a list rather than single object (for append-only operations)
- Include timestamp with ISO format
- Use 2-space indentation for readability
- Handle JSON decode errors gracefully
