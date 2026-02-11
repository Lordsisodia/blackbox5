# DECISIONS - Project Memory Migration

**Run:** run-20260119_100000

---

## Architectural Decisions

### DEC-001: 6-Folder Structure
**Decision:** Organize by question type, not file type
**Rationale:** AI agents think in questions, not file types
**Structure:** decisions/, knowledge/, operations/, plans/, project/, tasks/

### DEC-002: Remove Empty Folders
**Decision:** Remove domains/ folder (10 empty subfolders)
**Rationale:** YAGNI principle - create when needed
**Impact:** 67% reduction in folder count

### DEC-003: Consolidate YAML Files
**Decision:** Move FEATURE-BACKLOG.yaml and TEST-RESULTS.yaml to root
**Rationale:** Config files should be discoverable at root
**Previous:** plans/feature_backlog.yaml, knowledge/artifacts/test_results.yaml

## Scope Decisions

### DEC-004: agents/ Location
**Decision:** Move agents/ to operations/agents/
**Rationale:** Agents are part of system operations
**Impact:** Better categorization

### DEC-005: Root-Level Files
**Decision:** Keep essential files at root (ACTIVE.md, WORK-LOG.md, STATE.yaml)
**Rationale:** Quick access to current status
**Impact:** No navigation needed for status checks
