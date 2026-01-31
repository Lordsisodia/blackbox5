# Decisions - Loop 41

## DEC-41-1: Create PlanningAgent as Python class (not YAML)
**Context:** PLAN-003 planning agent implementation
**Options:**
- OPT-001: Create as YAML agent (simpler, declarative)
- OPT-002: Create as Python class (more flexibility, custom logic)
**Selected:** OPT-002
**Rationale:** Planning requires complex logic (task breakdown, agent assignment) that's easier to implement in Python. YAML agents are better for specialist personas with predefined behaviors.
**Reversibility:** LOW (can add YAML variant later)

## DEC-41-2: Defer LLM integration to future loops
**Context:** Planning generation requires intelligence
**Options:**
- OPT-001: Full LLM integration now (complex, time-consuming)
- OPT-002: Placeholder logic with structured output (fast, testable)
**Selected:** OPT-002
**Rationale:** Get the structure and integration working first. LLM can be added incrementally.
**Reversibility:** HIGH (easy to swap placeholder for LLM calls)

## DEC-41-3: Make Vibe Kanban optional
**Context:** PLAN-003 requires Vibe Kanban integration
**Options:**
- OPT-001: Hard dependency (fail if not configured)
- OPT-002: Optional with graceful skip
**Selected:** OPT-002
**Rationale:** Allows PlanningAgent to work independently. Vibe Kanban can be added via set_vibe_kanban() method.
**Reversibility:** LOW (already optional, can make required later)
