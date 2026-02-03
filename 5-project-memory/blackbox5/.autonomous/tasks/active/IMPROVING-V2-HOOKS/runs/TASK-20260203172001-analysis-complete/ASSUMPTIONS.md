# ASSUMPTIONS: TASK-20260203172001 - Hook Patterns Analysis

## Technical Assumptions

1. **UV Availability:** BB5 systems have uv installed for script execution
2. **Python 3.11+:** All hooks target Python 3.11 or higher
3. **Claude Code Support:** All 13 hooks are supported by current Claude Code version
4. **JSON stdin:** All hooks receive input via JSON on stdin

## BB5-Specific Assumptions

1. **Multi-Agent Environment:** RALF runs Executor, Planner, Architect concurrently
2. **Autonomous Operation:** Hooks must work without human intervention
3. **Log Directory:** logs/ directory is writable and persisted across sessions
4. **Context Injection:** additionalContext from SessionStart reaches Claude's prompt

## Pattern Adaptation Assumptions

1. **Security Customization:** User wants .env access for agents (may skip .env blocking)
2. **TTS Optional:** TTS features are optional, hooks work silently if TTS unavailable
3. **LLM Fallback:** Ollama local LLM available as fallback for task summarization
4. **Git Available:** Git commands available for SessionStart git status feature

## Scope Assumptions

1. **Mastery Repo Primary:** claude-code-hooks-mastery is primary source of patterns
2. **Other Repos Secondary:** Other 8 repos may provide additional patterns but not critical
3. **RALF Integration:** Patterns will integrate with existing RALF checkpoint-auto-save.sh
4. **Backward Compatibility:** New hooks don't break existing RALF functionality
