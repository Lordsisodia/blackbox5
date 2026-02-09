# DECISIONS: Research Pipeline System (RAPS)

## DEC-001: 4-Agent Pipeline Architecture
**Date:** 2026-02-04
**Status:** Accepted

**Decision:** Use 4 specialized agents (Scout → Analyst → Planner → Executor)

**Rationale:**
- Clear separation of concerns
- Each agent can be optimized independently
- Easier to debug and scale
- Matches pipeline pattern

**Alternatives:**
- 2-agent (too coarse, loses specialization)
- 6+ agent (overly complex, coordination overhead)

**Impact:** Clean boundaries, parallel development possible

---

## DEC-002: Hybrid Communication (Redis + Files)
**Date:** 2026-02-04
**Status:** Accepted

**Decision:** Use Redis for coordination, files for audit trail

**Rationale:**
- Redis: 1ms latency, perfect for agent coordination
- Files: Human-readable, persistent, auditable
- Best of Dual-RALF and BB5 Autonomous

**Tradeoffs:**
- (+) Speed + Auditability
- (+) Can debug by reading files
- (-) Slightly more complex
- (-) Need to keep in sync

**Impact:** All agents write to both Redis and files

---

## DEC-003: Neo4j for Concept Graph
**Date:** 2026-02-04
**Status:** Accepted

**Decision:** Use Neo4j graph database for concept relationships

**Rationale:**
- Natural fit for pattern relationships
- Powerful traversal queries
- Flexible schema evolution

**Alternatives:**
- PostgreSQL (poor graph traversal)
- MongoDB (no native relationships)
- Redis Graph (limited query capabilities)

**Impact:** New infrastructure component to maintain

---

## DEC-004: Continuous + Triggered Hybrid
**Date:** 2026-02-04
**Status:** Accepted

**Decision:** Scout/Analyst continuous, Planner/Executor triggered

**Rationale:**
- Scout needs to monitor continuously
- Analyst responds to new data
- Planner only needed on approval
- Executor should be capacity-controlled

**Tradeoffs:**
- (+) Cost efficiency
- (+) Appropriate responsiveness
- (-) More complex scheduling

**Impact:** Different deployment patterns per agent

---

## DEC-005: 4 Human Approval Gates
**Date:** 2026-02-04
**Status:** Accepted

**Decision:** Human gates at: concept review, recommendation, task plan, implementation

**Rationale:**
- Balance autonomy with oversight
- Catch errors early
- Build trust in system

**Tradeoffs:**
- (+) Risk mitigation
- (+) Quality control
- (-) Adds latency
- (-) Requires human availability

**Impact:** Auto-approval thresholds prevent bottlenecks

---

## DEC-006: Leverage BB5 Infrastructure
**Date:** 2026-02-04
**Status:** Accepted

**Decision:** Reuse TaskRegistry, RedisCoordinator, AgentOrchestrator, BMAD skills

**Rationale:**
- Proven, production-ready
- Faster development
- Consistent patterns

**Tradeoffs:**
- (+) Speed to market
- (+) Operational familiarity
- (-) Tightly coupled to BB5
- (-) Must work within constraints

**Impact:** Only build Scout, Analyst, and Neo4j integration

---

## DEC-007: Executor One-Task-At-A-Time
**Date:** 2026-02-04
**Status:** Accepted

**Decision:** Executor processes exactly one task concurrently

**Rationale:**
- Controlled compute costs
- Focus on quality over quantity
- Prevents resource contention

**Constraints:**
- Max concurrent: 1
- Max duration: 4 hours
- Daily limit: 3 tasks

**Impact:** Slower throughput, higher quality

---

## Open Decisions

1. **Scoring Thresholds:** What value/cost ratio triggers auto-approval?
2. **Source Priorities:** How to prioritize GitHub vs YouTube vs docs?
3. **Feedback Loop:** How to incorporate execution results into rankings?
4. **Conflict Resolution:** How to handle conflicting recommendations?

---

*Decisions evolve. Revisit after each phase.*
