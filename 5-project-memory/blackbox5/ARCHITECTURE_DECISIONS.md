# Architecture Decision Record (ADR)

**Project:** BlackBox5
**Purpose:** Track significant architecture decisions and their rationale

---

## How to Use This Document

### For Architects:
1. When proposing architecture change, create ADR entry
2. Status starts as "proposed"
3. After human review, update to "approved" or "rejected"
4. After implementation, update to "implemented"

### For Humans:
1. Review ADR entries with status "proposed"
2. To approve: Create file in `.autonomous/approvals/ADR-XXX-approved`
3. To reject: Add rejection rationale to ADR entry

---

## ADR Template

```markdown
## ADR-XXX: [Title]

**Date:** YYYY-MM-DD
**Status:** [proposed | approved | rejected | implemented | superseded]
**Deciders:** [names]

### Context
[What is the issue that we're seeing that is motivating this decision or change?]

### Decision
[What is the change that we're proposing or have agreed to implement?]

### Consequences
[What becomes easier or more difficult to do because of this change?]

### Options Considered
- Option A: [description] - rejected because [reason]
- Option B: [description] - selected because [reason]
- Option C: [description] - rejected because [reason]

### Implementation
- [ ] Phase 1: [description]
- [ ] Phase 2: [description]
- [ ] Verification: [description]

### Rollback Plan
[How to undo if things go wrong]
```

---

## Active Decisions

### ADR-001: [Example - Replace with real first decision]
**Date:** 2026-02-01
**Status:** proposed
**Context:** Multiple .autonomous directories causing confusion
**Decision:** TBD - awaiting analysis

---

## Implemented Decisions

[None yet - this section will grow]

---

## Rejected Decisions

[None yet - this section tracks decisions we considered but rejected]

---

## Superseded Decisions

[None yet - this section tracks decisions that were replaced by newer ones]
