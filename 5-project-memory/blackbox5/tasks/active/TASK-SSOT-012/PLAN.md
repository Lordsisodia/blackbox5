# PLAN.md: Merge Run Output Files

**Task:** TASK-SSOT-012 - Run output split across multiple files
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Run outputs are fragmented across multiple files:
- `runs/**/THOUGHTS.md` - Thoughts and reasoning
- `runs/**/DECISIONS.yaml` - Decisions made
- `runs/**/ASSUMPTIONS.md` - Assumptions
- `runs/**/RESULTS.md` - Results
- `runs/**/LEARNINGS.md` - Learnings

This creates:
1. **Fragmented Context**: Understanding a run requires reading multiple files
2. **Inconsistent Formats**: Mix of Markdown and YAML
3. **Query Complexity**: Hard to get complete run picture
4. **Navigation Overhead**: Constant file switching

### First Principles Solution
- **Unified Structure**: Single file with clear sections
- **Consistent Format**: One format (YAML or Markdown)
- **Machine Readable**: Structured for automated analysis
- **Human Readable**: Clear organization for humans

---

## 2. Current State Analysis

### File Structure

```
runs/run-20260205_143022/
├── THOUGHTS.md          # Free-form thoughts
├── DECISIONS.yaml       # Structured decisions
├── ASSUMPTIONS.md       # Assumptions
├── RESULTS.md           # Results
└── LEARNINGS.md         # Learnings
```

### Issues

1. **Too Many Files**: 5+ files per run
2. **Format Mixing**: Markdown + YAML
3. **Cross-References**: Content in one file references another
4. **Duplication**: Some content repeated across files

---

## 3. Proposed Solution

### Decision: Unified Run Output

**New Structure:** `runs/**/RUN.yaml`

```yaml
run_id: "run-20260205_143022"
timestamp: "2026-02-05T14:30:22Z"
task_id: "TASK-001"

thoughts:
  - timestamp: "2026-02-05T14:30:22Z"
    content: "Initial analysis of the problem..."
  - timestamp: "2026-02-05T14:35:00Z"
    content: "Considering alternative approaches..."

decisions:
  - id: "dec-001"
    timestamp: "2026-02-05T14:40:00Z"
    title: "Use PostgreSQL"
    rationale: "Better JSON support"
    reversibility: "MEDIUM"

assumptions:
  - id: "asm-001"
    content: "Database will handle expected load"
    risk_level: "LOW"
    verified: false

results:
  status: "completed"
  summary: "Successfully implemented feature"
  artifacts:
    - "src/feature.py"
    - "tests/test_feature.py"

learnings:
  - "Using SQLAlchemy simplifies migrations"
  - "Always test with realistic data volumes"
```

### Implementation Plan

#### Phase 1: Create Migration Script (2 hours)

**File:** `2-engine/.autonomous/bin/merge-run-files.py`

```python
#!/usr/bin/env python3
"""Merge run output files into unified RUN.yaml."""

import yaml
from pathlib import Path

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

    # Parse THOUGHTS.md
    thoughts_file = run_dir / 'THOUGHTS.md'
    if thoughts_file.exists():
        run_data['thoughts'] = parse_thoughts(thoughts_file)

    # Parse DECISIONS.yaml
    decisions_file = run_dir / 'DECISIONS.yaml'
    if decisions_file.exists():
        with open(decisions_file) as f:
            run_data['decisions'] = yaml.safe_load(f) or []

    # Parse ASSUMPTIONS.md
    assumptions_file = run_dir / 'ASSUMPTIONS.md'
    if assumptions_file.exists():
        run_data['assumptions'] = parse_assumptions(assumptions_file)

    # Parse RESULTS.md
    results_file = run_dir / 'RESULTS.md'
    if results_file.exists():
        run_data['results'] = parse_results(results_file)

    # Parse LEARNINGS.md
    learnings_file = run_dir / 'LEARNINGS.md'
    if learnings_file.exists():
        run_data['learnings'] = parse_learnings(learnings_file)

    # Write unified file
    output_file = run_dir / 'RUN.yaml'
    with open(output_file, 'w') as f:
        yaml.dump(run_data, f, default_flow_style=False)

    print(f"Created {output_file}")
```

#### Phase 2: Run Migration (1 hour)

1. Run migration script on all existing runs
2. Verify merged content
3. Handle edge cases

#### Phase 3: Update Templates (1 hour)

**New Template:** `RUN.yaml.template`

```yaml
run_id: "{{RUN_ID}}"
timestamp: "{{TIMESTAMP}}"
task_id: "{{TASK_ID}}"

thoughts: []
decisions: []
assumptions: []
results:
  status: "in_progress"
learnings: []
```

#### Phase 4: Deprecation (30 min)

1. Mark old files as deprecated
2. Update scripts to use RUN.yaml
3. Document migration

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/bin/merge-run-files.py` - Migration script
2. `.templates/run/RUN.yaml.template` - New run template

### Modified Files
1. Run initialization scripts
2. Run reading scripts

---

## 5. Success Criteria

- [ ] Migration script created and tested
- [ ] All historical runs merged to RUN.yaml
- [ ] New runs use unified format
- [ ] Old files marked as deprecated
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep old files alongside RUN.yaml
2. **Fix**: Debug merge logic
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Migration Script | 2 hours | 2 hours |
| Phase 2: Run Migration | 1 hour | 3 hours |
| Phase 3: Templates | 1 hour | 4 hours |
| Phase 4: Deprecation | 30 min | 4.5 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Run output fragmented*
