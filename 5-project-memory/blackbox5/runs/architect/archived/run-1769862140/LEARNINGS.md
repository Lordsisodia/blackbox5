# Learnings - Loop 41

## Agent System Structure
- Agents defined in ~/.blackbox5/2-engine/core/agents/definitions/
- BaseAgent provides execute_with_hooks() which handles validation, timing, status
- Required methods: execute() and think()
- Optional hooks: before_execution, after_execution, validate_task

## Import Patterns
- Use relative imports within definitions package: `from .core.base_agent`
- AgentConfig, AgentTask, AgentResult are in base_agent.py (not separate file)

## Testing Approach
- Test by importing to verify syntax
- Test by creating instance to verify __init__
- Test by calling execute_with_hooks() to verify full flow
- Check artifacts structure

## Agent-2.5 Simplification Benefits
- Quick Flow (3 phases) vs Full BMAD (5 phases) - perfect for single class creation
- Focus on "does it work together?" vs comprehensive testing
- Get structure working, iterate from there
