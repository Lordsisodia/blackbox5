# DECISIONS - Loop 44 - BMAD Framework Implementation

## Decision 1: Use Heuristics Instead of LLM
**Context**: BMAD modules need to extract information from user requests.
**Options**:
- OPT-001: Use LLM API calls (requires external service, cost, latency)
- OPT-002: Use heuristic/pattern matching (fast, local, predictable)
**Selected**: OPT-002 (heuristics)
**Rationale**: Fast, local, no external dependencies. LLM integration can be added as a enhancement layer.
**Reversibility**: LOW - easily swapped for LLM later via subclass or config.

## Decision 2: Async Architecture
**Context**: PlanningAgent uses async, should BMAD follow?
**Options**:
- OPT-001: Sync methods (simpler, but inconsistent)
- OPT-002: Async methods (consistent with PlanningAgent)
**Selected**: OPT-002 (async)
**Rationale**: Consistency with PlanningAgent, future-proof for LLM integration.
**Reversibility**: LOW - async functions can be called synchronously if needed.

## Decision 3: Optional BMAD in PlanningAgent
**Context**: Should BMAD be mandatory or optional?
**Options**:
- OPT-001: Always enabled (simpler, less flexible)
- OPT-002: Configurable via metadata (more flexible)
**Selected**: OPT-002 (configurable)
**Rationale**: Allows testing without BMAD, fallback if BMAD fails.
**Reversibility**: HIGH - easily removed by removing the conditional.

## Decision 4: Separate Module Files
**Context**: How to structure BMAD code?
**Options**:
- OPT-001: Single file with all classes (simpler, larger file)
- OPT-002: Separate files per dimension (more files, cleaner separation)
**Selected**: OPT-002 (separate files)
**Rationale**: Clear separation of concerns, easier to maintain, follows existing patterns.
**Reversibility**: LOW - file structure is established but not irreversible.

## Decision 5: Fix tech_stack Handling Bug
**Context**: Test failed because context["tech_stack"] was a list, not dict.
**Options**:
- OPT-001: Only accept dict (breaking change)
- OPT-002: Handle both dict and list (flexible)
**Selected**: OPT-002 (handle both)
**Rationale**: List is a natural way to pass tech stack. No breaking change.
**Reversibility**: LOW - simple if/else logic.
