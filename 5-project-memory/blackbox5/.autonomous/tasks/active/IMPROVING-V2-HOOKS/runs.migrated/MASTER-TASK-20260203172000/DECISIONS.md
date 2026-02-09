# DECISIONS: MASTER-TASK-20260203172000 - Improving v2 Hooks

## Epic Structure
**Date:** 2026-02-04
**Decision:** Create master task with 5 subtasks, each with own run folder
**Rationale:** Parallel execution possible, clear ownership, traceable progress
**Impact:** 6 run folders created with full BB5 structure

## Source Selection
**Date:** 2026-02-04
**Decision:** Use claude-code-hooks-mastery as primary source (92/100 rating)
**Rationale:** Most comprehensive hook implementation, production-ready patterns
**Impact:** All 13 hooks analyzed, patterns catalogued

## Implementation Order
**Date:** 2026-02-04
**Decision:** Critical → High priority sequence
**Rationale:** Security first, then core functionality, then enhancements
**Impact:** Execution order: Security → SessionStart → JSON Logging → Subagent Tracking

## Pattern Adoption
**Date:** 2026-02-04
**Decision:** Adopt UV scripts, JSON logging, exit code 2 blocking, TTS locking
**Rationale:** These are proven patterns from mastery repo
**Impact:** BB5 hooks will follow mastery patterns
