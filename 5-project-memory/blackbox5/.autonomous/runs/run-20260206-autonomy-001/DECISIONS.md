# Decisions: TASK-AUTONOMY-001

## Decision 1: State Machine States
**Decision:** Use 6 states: pending → claimed → in_progress → completed → archived
**Rationale:** Matches TASK-ARCH-015 design. "claimed" separates intent from action.
**Date:** 2026-02-06

## Decision 2: Hook-Based Enforcement
**Decision:** State transitions enforced in hooks, not suggested to LLMs
**Rationale:** Critical Blocker #2 - LLMs cannot reliably follow instructions
**Date:** 2026-02-06

## Decision 3: Self-Discovery Pattern
**Decision:** Hooks detect task from current directory, no env vars
**Rationale:** More reliable than environment variables that may not be set
**Date:** 2026-02-06
