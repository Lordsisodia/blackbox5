# PLAN.md: Standardize Scout Report Format

**Task:** TASK-SSOT-014 - Scout reports in inconsistent formats
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Scout reports exist in multiple formats:
- `scout-report-*.json` - JSON format
- `scout-report-*.yaml` - YAML format
- `scout-report-*.md` - Markdown format
- Different schemas between reports

This creates:
1. **Parsing Complexity**: Need multiple parsers
2. **Inconsistent Data**: Same data in different structures
3. **Query Difficulty**: Hard to aggregate across reports
4. **Maintenance Overhead**: Multiple format support

### First Principles Solution
- **Single Format**: One canonical format (YAML recommended)
- **Standard Schema**: Consistent structure across all reports
- **Validation**: Schema validation for all reports
- **Migration**: Convert existing reports to standard format

---

## 2. Current State Analysis

### Report Locations

```
5-project-memory/blackbox5/.autonomous/analysis/scout-reports/
├── scout-report-20260205-013135.json
├── scout-report-20260205-013135.yaml
├── scout-report-20260205-013356.json
└── scout-report-aggregated.yaml
```

### Format Variations

**JSON Format:**
```json
{
  "timestamp": "2026-02-05T01:31:35Z",
  "findings": [...]
}
```

**YAML Format:**
```yaml
timestamp: "2026-02-05T01:31:35Z"
findings:
  - ...
```

**Markdown Format:**
```markdown
# Scout Report

**Timestamp:** 2026-02-05T01:31:35Z

## Findings
...
```

---

## 3. Proposed Solution

### Decision: Standard YAML Format

**Standard Schema:**

```yaml
version: "1.0"
report_id: "scout-20260205-013135"
timestamp: "2026-02-05T01:31:35Z"
scout_type: "intelligent"  # intelligent, quick, deep

metadata:
  task_id: "TASK-001"
  agent: "scout-intelligent"
  duration_seconds: 120

summary:
  total_files_scanned: 150
  issues_found: 12
  recommendations: 5

findings:
  - id: "F-001"
    severity: "HIGH"
    category: "security"
    file: "config.yaml"
    line: 45
    description: "Hardcoded credential found"
    recommendation: "Move to environment variable"

  - id: "F-002"
    severity: "MEDIUM"
    category: "performance"
    file: "main.py"
    line: 120
    description: "Inefficient loop detected"
    recommendation: "Use list comprehension"

recommendations:
  - priority: 1
    action: "Fix hardcoded credentials"
    effort: "1 hour"
    impact: "HIGH"
```

### Implementation Plan

#### Phase 1: Define Schema (1 hour)

**File:** `2-engine/.autonomous/lib/scout_report_schema.yaml`

Define complete schema with:
- Required fields
- Field types
- Validation rules
- Example report

#### Phase 2: Create Migration Script (1 hour)

**File:** `2-engine/.autonomous/bin/standardize-scout-reports.py`

```python
#!/usr/bin/env python3
"""Standardize all scout reports to YAML format."""

import json
import yaml
from pathlib import Path

def migrate_report(report_path: Path):
    """Migrate a single report to standard format."""
    # Load existing report
    if report_path.suffix == '.json':
        with open(report_path) as f:
            data = json.load(f)
    elif report_path.suffix == '.yaml':
        with open(report_path) as f:
            data = yaml.safe_load(f)
    else:
        return  # Skip markdown for now

    # Transform to standard schema
    standard = transform_to_standard(data)

    # Write as YAML
    output_path = report_path.with_suffix('.yaml')
    with open(output_path, 'w') as f:
        yaml.dump(standard, f, default_flow_style=False)

    print(f"Migrated {report_path} -> {output_path}")
```

#### Phase 3: Run Migration (1 hour)

1. Run migration on all existing reports
2. Validate converted reports
3. Archive old format files

#### Phase 4: Update Scout Scripts (1 hour)

Update all scout agents to output standard format:
- `scout-intelligent.py`
- `scout-task-based.py`
- Any other scout scripts

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/scout_report_schema.yaml` - Schema definition
2. `2-engine/.autonomous/bin/standardize-scout-reports.py` - Migration script

### Modified Files
1. Scout agent scripts
2. Report reading/processing scripts

---

## 5. Success Criteria

- [ ] Standard schema defined and documented
- [ ] All reports migrated to YAML format
- [ ] Schema validation implemented
- [ ] Scout agents output standard format
- [ ] Old format files archived

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep old format files
2. **Fix**: Debug migration script
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Schema | 1 hour | 1 hour |
| Phase 2: Migration Script | 1 hour | 2 hours |
| Phase 3: Run Migration | 1 hour | 3 hours |
| Phase 4: Update Scouts | 1 hour | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Scout reports in inconsistent formats*
