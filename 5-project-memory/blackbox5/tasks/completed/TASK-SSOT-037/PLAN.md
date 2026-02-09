# PLAN.md: Centralize Decision Registry

**Task:** TASK-SSOT-037 - Decisions scattered across run folders
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-5 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
Decisions are scattered:
- `runs/**/DECISIONS.yaml` - Per-run decisions
- `runs/**/THOUGHTS.md` - Embedded decisions
- No central decision registry

This creates:
1. **Discovery Difficulty**: Hard to find all decisions
2. **No History**: Can't see decision evolution
3. **No Aggregation**: Can't analyze decision patterns
4. **Inconsistent Format**: Different formats in different places

### First Principles Solution
- **Central Registry**: Single decision database
- **Structured Format**: Consistent decision schema
- **Searchable**: Query decisions by criteria
- **Referential**: Link to runs and tasks

---

## 2. Proposed Solution

### Central Decision Registry

**File:** `5-project-memory/blackbox5/.autonomous/decisions.yaml`

```yaml
version: "1.0"
description: "Central decision registry"

# Schema definition
schema:
  decision:
    required: [id, timestamp, phase, selected_option, rationale]
    optional: [options_considered, assumptions, reversibility, rollback_steps]

# All decisions
decisions:
  - id: "dec-2026020501"
    timestamp: "2026-02-05T10:00:00Z"
    task_id: "TASK-001"
    run_id: "run-20260205_100000"
    agent: "claude"

    phase: "PLAN"  # ALIGN, PLAN, EXECUTE, VALIDATE, WRAP

    context: |
      Need to choose database for new feature.
      Requirements: JSON support, scalability.

    options_considered:
      - option: "PostgreSQL"
        pros: ["JSON support", "Scalable", "Reliable"]
        cons: ["More complex", "Requires setup"]

      - option: "SQLite"
        pros: ["Simple", "No setup"]
        cons: ["Limited concurrency", "No JSON"]

    selected_option: "PostgreSQL"

    rationale: |
      PostgreSQL meets all requirements. JSON support
      is essential for flexible schema. Scalability
      ensures we won't need to migrate later.

    assumptions:
      - assumption: "Team knows PostgreSQL"
        risk_level: "LOW"
        verified: true

    reversibility: "MEDIUM"
    rollback_steps:
      - "Export data to SQL"
      - "Import to SQLite"
      - "Update connection strings"

    verification:
      criteria:
        - "Database deployed"
        - "Migrations run successfully"
        - "Tests pass"
      verified_at: "2026-02-05T12:00:00Z"
      verified_by: "verifier-agent"

# Indexes (generated)
indexes:
  by_task:
    TASK-001: ["dec-2026020501", "dec-2026020502"]
  by_phase:
    PLAN: ["dec-2026020501"]
  by_reversibility:
    MEDIUM: ["dec-2026020501"]
```

### Implementation Plan

#### Phase 1: Create Registry Schema (1 hour)

1. Define decision structure
2. Include all fields from decision_registry.py
3. Add indexing support

#### Phase 2: Create Migration Script (2 hours)

```python
def migrate_decisions(project_path: Path):
    """Migrate decisions from run folders to registry."""
    registry = {'version': '1.0', 'decisions': []}

    runs_dir = project_path / 'runs'
    for run_dir in runs_dir.iterdir():
        decisions_file = run_dir / 'DECISIONS.yaml'
        if decisions_file.exists():
            decisions = yaml.safe_load(decisions_file.read_text())
            for decision in decisions:
                decision['run_id'] = run_dir.name
                registry['decisions'].append(decision)

    # Sort by timestamp
    registry['decisions'].sort(key=lambda d: d['timestamp'])

    # Generate indexes
    registry['indexes'] = generate_indexes(registry['decisions'])

    # Save registry
    with open(project_path / '.autonomous' / 'decisions.yaml', 'w') as f:
        yaml.dump(registry, f)
```

#### Phase 3: Update Decision Recording (1 hour)

Update decision registry to write to central file:
```python
class DecisionRegistry:
    def record(self, decision: Decision):
        # Write to central registry
        registry = load_central_registry()
        registry['decisions'].append(decision.to_dict())
        save_central_registry(registry)
```

#### Phase 4: Create Query Interface (1 hour)

```python
def find_decisions(
    task_id: Optional[str] = None,
    phase: Optional[str] = None,
    reversibility: Optional[str] = None
) -> List[Dict]:
    """Query decisions from registry."""
    registry = load_central_registry()
    decisions = registry['decisions']

    if task_id:
        decisions = [d for d in decisions if d.get('task_id') == task_id]
    if phase:
        decisions = [d for d in decisions if d.get('phase') == phase]

    return decisions
```

---

## 3. Success Criteria

- [ ] Central registry created
- [ ] All decisions migrated
- [ ] Decision recording updated
- [ ] Query interface working

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Schema | 1 hour |
| Migration | 2 hours |
| Recording | 1 hour |
| Queries | 1 hour |
| **Total** | **4-5 hours** |

---

*Plan created based on SSOT violation analysis*
