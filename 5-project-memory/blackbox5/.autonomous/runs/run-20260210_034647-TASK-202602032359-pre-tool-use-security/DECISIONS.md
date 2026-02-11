# DECISIONS

## Design Decisions

### 1. Exit Code Semantics
**Decision**: Use exit code 2 for blocking
- `exit 0` = Allow tool execution
- `exit 2` = Block tool with error message to stderr

**Rationale**: This is the pattern established in the mastery repo and is standard for security hooks.

### 2. Command Normalization
**Decision**: Convert commands to lowercase and normalize spaces before pattern matching

**Rationale**: Ensures consistent matching regardless of user input (e.g., "rm -RF" vs "rm -rf").

### 3. Dangerous Path Detection
**Decision**: Include multiple dangerous paths in rm detection: /, ~, $HOME, .., wildcards

**Rationale**: Autonomously operating systems might reference these paths; blocking them prevents catastrophic damage.

### 4. .env Protection
**Decision**: Block .env file access (except .env.sample)

**Rationale**: .env files contain sensitive credentials; this is a common security best practice.

### 5. Modular Design
**Decision**: Create separate security_patterns.py utility module

**Rationale**: Allows reuse across multiple hooks, reducing code duplication and maintaining consistency.

### 6. Error Handling
**Decision**: Gracefully handle JSONDecodeError and other exceptions

**Rationale**: Hook errors should not break the entire system; log and exit 0 to allow normal operation.

## Integration Decisions

### Hook Registration
**Decision**: Register hook in .claude/settings.json

**Rationale**: Standard location for hook configuration in Claude Code.

### Logging Location
**Decision**: Log to logs/pre_tool_use.json in project root

**Rationale**: Centralized location for all tool call audit logs.
