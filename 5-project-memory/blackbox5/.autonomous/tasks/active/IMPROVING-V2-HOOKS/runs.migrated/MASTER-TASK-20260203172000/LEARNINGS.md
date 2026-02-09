# LEARNINGS: MASTER-TASK-20260203172000 - Improving v2 Hooks

## Coordination Learnings

### Subtask Organization
Creating individual run folders for each subtask provides:
- Clear separation of concerns
- Parallel work capability
- Individual traceability
- Easier rollback if needed

### Pattern Catalog Value
Having HOOKS-PATTERNS-CATALOG.md as central reference:
- Prevents re-analysis
- Ensures consistency
- Speeds up implementation
- Documents decisions

## Technical Learnings

### Hook Lifecycle
Understanding when each hook fires:
- SessionStart: Once at session start
- UserPromptSubmit: Before each user message
- PreToolUse: Before each tool call (can block)
- PostToolUse: After each tool call
- SubagentStart/Stop: Around subagent execution
- Stop: At session end

### Exit Code Criticality
Exit code 2 is the only way to block in PreToolUse. This is essential for security.

## Process Learnings

### Analysis Before Implementation
Documenting patterns first prevents:
- Missing important features
- Inconsistent implementations
- Rework and refactoring

### Task Template Importance
Using proper task format with timestamps ensures:
- Traceability
- Proper ordering
- Clear priorities
