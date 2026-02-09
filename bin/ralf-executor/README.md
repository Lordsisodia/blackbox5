# RALF Executor - BB5 Autonomous Task Execution Engine

The RALF Executor is the core execution engine for BlackBox5's autonomous task processing system. It handles the complete lifecycle of task execution from acquisition to completion.

## Features

- **Task Queue Management**: Automatically discovers and prioritizes pending tasks
- **Context Gathering**: Spawns bb5-context-collector agent for comprehensive context
- **Dynamic Prompt Building**: Creates execution prompts tailored to each task
- **Claude Code Integration**: Executes tasks via `claude -p --dangerously-skip-permissions`
- **Run Documentation**: Auto-generates THOUGHTS.md, DECISIONS.md, LEARNINGS.md, RESULTS.md, CHANGES.md
- **Git Integration**: Commits changes automatically with descriptive messages
- **Completion Verification**: Checks for `<promise>COMPLETE</promise>` signal
- **Dry Run Mode**: Test execution without making changes

## Usage

```bash
# Basic execution (process next pending task)
python3 bin/ralf-executor/executor.py

# Dry run mode (no actual changes)
python3 bin/ralf-executor/executor.py --dry-run

# Verbose logging
python3 bin/ralf-executor/executor.py --verbose

# Execute specific task
python3 bin/ralf-executor/executor.py --task-id TASK-2026-01-18-005
```

## Task Lifecycle

1. **Acquire Task**: Scans `tasks/active/` for pending tasks, selects highest priority
2. **Lock Task**: Updates status to `claimed` to prevent duplicate execution
3. **Create Run Folder**: Creates `runs/executor/run-YYYYMMDD_HHMMSS-TASK-XXX/`
4. **Initialize Docs**: Creates THOUGHTS.md, DECISIONS.md, LEARNINGS.md, RESULTS.md, CHANGES.md
5. **Gather Context**: Spawns bb5-context-collector agent
6. **Build Prompt**: Creates dynamic execution prompt with task details and context
7. **Execute**: Runs Claude Code with the prompt
8. **Monitor**: Waits for completion signal (`<promise>COMPLETE</promise>`)
9. **Verify**: Checks acceptance criteria completion
10. **Complete**: Updates task status, moves to completed/, commits changes

## Task Status Flow

```
pending → claimed → in_progress → [completed | partial | failed]
```

## Directory Structure

```
runs/executor/
└── run-YYYYMMDD_HHMMSS-TASK-XXX/
    ├── THOUGHTS.md          # Execution thoughts and reasoning
    ├── DECISIONS.md         # Decisions made during execution
    ├── LEARNINGS.md         # What was learned
    ├── RESULTS.md           # Execution results and acceptance criteria status
    ├── CHANGES.md           # Files modified and git commit info
    ├── CONTEXT_REPORT.md    # Output from context collector
    ├── execution_prompt.md  # Prompt sent to Claude Code
    └── claude_output.log    # Raw Claude Code output
```

## Configuration

The executor uses these paths (configurable in the script):

- `BB5_DIR`: `/Users/shaansisodia/.blackbox5`
- `TASKS_DIR`: `BB5_DIR/5-project-memory/siso-internal/tasks`
- `RUNS_DIR`: `BB5_DIR/runs/executor`
- `AGENTS_DIR`: `BB5_DIR/.claude/agents`

## Task File Format

Tasks are markdown files with frontmatter-style metadata:

```markdown
# TASK-XXX: Task Title

**Status:** pending
**Priority:** high
**Type:** github-integration
**Created:** 2026-01-18T00:00:00Z

## Description

Task description here...

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies

- TASK-XXX-001
```

## Error Handling

- **Task Parse Errors**: Logged as warnings, task skipped
- **Context Collector Failure**: Execution continues without context
- **Claude Code Timeout**: Task marked as partial
- **Git Errors**: Logged but don't fail the task
- **Keyboard Interrupt**: Graceful shutdown with exit code 130

## Exit Codes

- `0`: Task completed successfully
- `1`: Task completed partially or failed
- `130`: Interrupted by user

## Dependencies

- Python 3.8+
- PyYAML (`pip install pyyaml`)
- Claude Code CLI (`claude`)
- Git

## Integration with BB5 Agent Teams

The executor works with the BB5 agent ecosystem:

- **bb5-context-collector**: Gathers comprehensive context before execution
- **bb5-superintelligence**: Can be invoked for complex decisions
- **bb5-scribe**: Documents all activity (integrated into executor's doc generation)

## Testing

```bash
# Test with dry run
python3 bin/ralf-executor/executor.py --dry-run --verbose

# Test specific task
python3 bin/ralf-executor/executor.py --task-id TASK-2026-01-18-005 --dry-run
```
