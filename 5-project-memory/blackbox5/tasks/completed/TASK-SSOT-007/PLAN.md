# PLAN.md: Extract Decisions from THOUGHTS.md to DECISIONS.yaml

**Task:** TASK-SSOT-007 - Decisions embedded in THOUGHTS.md instead of DECISIONS.yaml
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-6 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Decisions are currently embedded in:
- `5-project-memory/blackbox5/runs/**/THOUGHTS.md` - Mixed with thoughts

Instead of being in:
- `5-project-memory/blackbox5/runs/**/DECISIONS.yaml` - Structured decisions

This creates:
1. **Discovery Difficulty**: Finding decisions requires parsing prose
2. **No Structure**: Decisions lack consistent format
3. **No Metadata**: Missing timestamps, rationales, reversibility
4. **Query Complexity**: Cannot easily query decision history

### First Principles Solution
- **Structured Decisions**: Use DECISIONS.yaml format
- **Machine Readable**: Enable automated analysis
- **Rich Metadata**: Include context, rationale, reversibility
- **Migration**: Extract existing decisions from THOUGHTS.md

---

## 2. Current State Analysis

### File Structure

```
runs/run-20260205_143022/
├── THOUGHTS.md          # Contains embedded decisions
├── DECISIONS.yaml       # Exists but may be empty/underused
├── ASSUMPTIONS.md
└── RESULTS.md
```

### THOUGHTS.md Decision Patterns

Decisions typically appear as:
```markdown
## Decision: Use PostgreSQL

After considering SQLite and MySQL, I've decided to use PostgreSQL.
Rationale: Better JSON support, more robust.

**Decision**: PostgreSQL for primary database.
```

---

## 3. Proposed Solution

### Step 1: Create Extraction Script (2 hours)

**File:** `2-engine/.autonomous/bin/extract-decisions.py`

```python
#!/usr/bin/env python3
"""Extract decisions from THOUGHTS.md files to DECISIONS.yaml."""

import re
import yaml
from pathlib import Path
from datetime import datetime

DECISION_PATTERNS = [
    r'##\s*Decision:\s*(.+?)\n\n(.+?)(?=\n##|\Z)',  # ## Decision: Title\n\ncontent
    r'\*\*Decision\*\*:\s*(.+?)(?=\n\*\*|\n##|\Z)',  # **Decision**: content
]

def extract_decisions(thoughts_path: Path) -> list:
    """Extract decisions from a THOUGHTS.md file."""
    content = thoughts_path.read_text()
    decisions = []

    for pattern in DECISION_PATTERNS:
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            decisions.append({
                'title': match.group(1).strip(),
                'description': match.group(2).strip() if len(match.groups()) > 1 else '',
                'extracted_from': str(thoughts_path),
                'extracted_at': datetime.now().isoformat(),
            })

    return decisions

def migrate_run_decisions(run_dir: Path):
    """Migrate decisions for a single run."""
    thoughts_path = run_dir / 'THOUGHTS.md'
    decisions_path = run_dir / 'DECISIONS.yaml'

    if not thoughts_path.exists():
        return

    decisions = extract_decisions(thoughts_path)

    if decisions:
        existing = []
        if decisions_path.exists():
            existing = yaml.safe_load(decisions_path.read_text()) or []

        all_decisions = existing + decisions

        with open(decisions_path, 'w') as f:
            yaml.dump(all_decisions, f, default_flow_style=False)

        print(f"Migrated {len(decisions)} decisions in {run_dir.name}")
```

### Step 2: Run Migration (1 hour)

1. Run extraction script on all run folders
2. Verify extracted decisions
3. Handle edge cases

### Step 3: Update Templates (1 hour)

**Update:** Run initialization templates

```markdown
# THOUGHTS.md.template

<!-- Thoughts go here - do NOT include decisions -->
<!-- Use DECISIONS.yaml for all decisions -->
```

### Step 4: Update Documentation (1 hour)

1. Document decision format
2. Update agent prompts to use DECISIONS.yaml
3. Add validation to ensure decisions aren't in THOUGHTS.md

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/bin/extract-decisions.py` - Migration script

### Modified Files
1. Run templates (remove decision sections from THOUGHTS.md)
2. Agent prompts (reference DECISIONS.yaml)

---

## 5. Success Criteria

- [ ] Extraction script created and tested
- [ ] All historical decisions extracted from THOUGHTS.md
- [ ] DECISIONS.yaml populated for all runs
- [ ] Templates updated to separate concerns
- [ ] Documentation updated
- [ ] Validation prevents new decisions in THOUGHTS.md

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore original THOUGHTS.md files
2. **Fix**: Debug extraction script
3. **Re-run**: Once fixed

---

## 7. Estimated Timeline

| Step | Duration | Cumulative |
|------|----------|------------|
| Step 1: Extraction Script | 2 hours | 2 hours |
| Step 2: Migration | 1 hour | 3 hours |
| Step 3: Templates | 1 hour | 4 hours |
| Step 4: Documentation | 1 hour | 5 hours |
| **Total** | | **4-6 hours** |

---

*Plan created based on SSOT violation analysis - Decisions in THOUGHTS.md*
