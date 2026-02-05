# PLAN.md: Merge Run Output Files

**Task:** TASK-SSOT-034 - Run output fragmented across multiple files
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Run outputs are split across:
- `THOUGHTS.md` - Thoughts and reasoning
- `DECISIONS.yaml` - Decisions made
- `ASSUMPTIONS.md` - Assumptions
- `RESULTS.md` - Results
- `LEARNINGS.md` - Learnings

This creates:
1. **Fragmented Context**: Need to read multiple files
2. **Inconsistent Formats**: Mix of Markdown and YAML
3. **Query Complexity**: Hard to get complete picture
4. **Navigation Overhead**: Constant file switching

### First Principles Solution
- **Unified Structure**: Single file with sections
- **Consistent Format**: One format (YAML)
- **Machine Readable**: Structured for automation
- **Human Readable**: Clear organization

---

## 2. Proposed Solution

### Unified Run Format

**File:** `runs/**/RUN.yaml`

```yaml
run_id: "run-20260205_143022"
timestamp: "2026-02-05T14:30:22Z"
task_id: "TASK-001"
agent: "claude"

thoughts:
  - timestamp: "2026-02-05T14:30:22Z"
    content: "Initial analysis..."
  - timestamp: "2026-02-05T14:35:00Z"
    content: "Considering alternatives..."

decisions:
  - id: "dec-001"
    timestamp: "2026-02-05T14:40:00Z"
    title: "Use PostgreSQL"
    rationale: "Better JSON support"
    reversibility: "MEDIUM"

assumptions:
  - id: "asm-001"
    content: "Database will handle load"
    risk_level: "LOW"
    verified: false

results:
  status: "completed"
  summary: "Successfully implemented"
  artifacts:
    - "src/feature.py"

learnings:
  - "SQLAlchemy simplifies migrations"
  - "Test with realistic data"
```

### Implementation Plan

#### Phase 1: Create Migration Script (2 hours)

```python
def merge_run_files(run_dir: Path):
    """Merge all run files into RUN.yaml."""
    run_data = {
        'run_id': run_dir.name,
        'thoughts': [],
        'decisions': [],
        'assumptions': [],
        'results': {},
        'learnings': []
    }

    # Parse each file and merge
    if (run_dir / 'THOUGHTS.md').exists():
        run_data['thoughts'] = parse_thoughts(run_dir / 'THOUGHTS.md')

    if (run_dir / 'DECISIONS.yaml').exists():
        run_data['decisions'] = yaml.safe_load(
            (run_dir / 'DECISIONS.yaml').read_text()
        )

    # ... similar for other files

    # Write unified file
    with open(run_dir / 'RUN.yaml', 'w') as f:
        yaml.dump(run_data, f)
```

#### Phase 2: Run Migration (1 hour)

1. Run on all existing runs
2. Verify merged content
3. Handle edge cases

#### Phase 3: Update Templates (1 hour)

Create new run template using unified format.

---

## 3. Success Criteria

- [ ] Migration script created
- [ ] All runs migrated
- [ ] New template created
- [ ] Documentation updated

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Script | 2 hours |
| Migration | 1 hour |
| Templates | 1 hour |
| **Total** | **3-4 hours** |

---

*Plan created based on SSOT violation analysis*
