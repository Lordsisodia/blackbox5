# DECISIONS - BlackBox5 Structure Alignment

**Run:** run-20260209_143000

---

## Structural Decisions

### DEC-001: Match BlackBox5 Structure
**Decision:** Align SISO-Internal data/, learnings/, runs/ with BlackBox5
**Rationale:** Consistency across projects enables better tooling
**Impact:** All projects use same structure

### DEC-002: Example Run Content
**Decision:** Create 5 example runs based on actual project history
**Rationale:** Demonstrates different run types with realistic content
**Runs:**
1. Feature Planning (User Profile PRD)
2. Architecture (Epic Creation)
3. Infrastructure (Project Memory Migration)
4. GitHub Integration (Sync Operation)
5. Current run (Structure Alignment)

### DEC-003: Learning Organization
**Decision:** Organize learnings by type (patterns, first_principles, improvements, retrospectives)
**Rationale:** Easier to find relevant insights
**Alternative:** Chronological only (rejected - harder to browse)

## Content Decisions

### DEC-004: Recent Learnings Format
**Decision:** Use same format as BlackBox5 recent.md
**Rationale:** Familiar structure for agents
**Template:** Date, Discovery, Impact, Action, Details

### DEC-005: Run File Set
**Decision:** Include 5 files per run (THOUGHTS, DECISIONS, RESULTS, LEARNINGS, ASSUMPTIONS)
**Rationale:** Based on BlackBox5 analysis showing these are most used
**Files not included:** metadata.yaml (can be added when needed)
