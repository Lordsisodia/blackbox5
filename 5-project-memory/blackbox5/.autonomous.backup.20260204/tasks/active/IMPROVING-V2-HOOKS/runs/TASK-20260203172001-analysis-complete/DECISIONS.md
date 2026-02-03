# DECISIONS: TASK-20260203172001 - Hook Patterns Analysis

## Decision 1: Parallel Analysis Approach
**Date:** 2026-02-04
**Decision:** Spawn 4 subagents simultaneously to analyze different hook categories
**Rationale:** Faster completion, specialized focus per agent, comprehensive coverage
**Impact:** Analysis completed in single session instead of sequential review

## Decision 2: Document Before Implement
**Date:** 2026-02-04
**Decision:** Create comprehensive patterns catalog before writing any implementation code
**Rationale:** Ensures no patterns are missed, provides reference for all implementation tasks
**Impact:** HOOKS-PATTERNS-CATALOG.md serves as single source of truth

## Decision 3: UV Script Pattern Adoption
**Date:** 2026-02-04
**Decision:** Adopt PEP 723 UV single-file script pattern for all new hooks
**Rationale:** Self-contained, no virtualenv management, fast execution
**Impact:** All BB5 hooks will use this pattern going forward

## Decision 4: TTS Priority Chain
**Date:** 2026-02-04
**Decision:** Implement ElevenLabs > OpenAI > pyttsx3 priority chain
**Rationale:** Best quality first, fallback to local TTS if no API keys
**Impact:** Consistent TTS behavior across all hooks

## Decision 5: File-Based Locking for Multi-Agent
**Date:** 2026-02-04
**Decision:** Use fcntl.flock for TTS queue management in multi-agent RALF
**Rationale:** Cross-process synchronization essential for concurrent agents
**Impact:** Prevents TTS collisions when Executor/Planner/Architect run simultaneously

## Decision 6: Exit Code 2 for Security Blocking
**Date:** 2026-02-04
**Decision:** Use exit code 2 to block dangerous commands in pre_tool_use hook
**Rationale:** Only way to prevent tool execution and show error to Claude
**Impact:** Security hook can actually block rm -rf and .env access

## Decision 7: JSON Logging Standardization
**Date:** 2026-02-04
**Decision:** All hooks use identical read-modify-write JSON logging pattern
**Rationale:** Consistent log format enables aggregation and analysis
**Impact:** Standardized logs in logs/ directory for all hook events
