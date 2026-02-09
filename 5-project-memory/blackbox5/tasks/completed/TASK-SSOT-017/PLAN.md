# PLAN.md: Extract Analysis from Reports Pipeline

**Task:** TASK-SSOT-017 - Analysis data embedded in report files
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-5 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Analysis data is embedded within larger report files:
- Scout reports contain analysis + raw data
- Verifier reports contain analysis + test results
- Executor reports contain analysis + implementation details

This creates:
1. **Extraction Difficulty**: Hard to get just the analysis
2. **Mixed Concerns**: Raw data and analysis in same file
3. **Query Complexity**: Can't query analysis separately
4. **Duplication**: Same analysis in multiple reports

### First Principles Solution
- **Separation of Concerns**: Analysis separate from raw data
- **Structured Analysis**: Standard analysis format
- **Referential Integrity**: Analysis references source data
- **Aggregation**: Easy to aggregate analysis across reports

---

## 2. Current State Analysis

### Report Structure

```yaml
# scout-report-20260205.yaml
version: "1.0"
report_id: "scout-20260205"

# Raw data
files_scanned:
  - path: "src/main.py"
    lines: 150
    issues: [...]

# Analysis embedded in findings
findings:
  - id: "F-001"
    analysis: "This issue indicates a security vulnerability..."
    recommendation: "Fix by moving to env vars"

# More raw data
summary:
  total_files: 150
  total_issues: 12
```

### Issues

1. **Mixed Content**: Raw data and analysis together
2. **No Clear Separation**: Hard to extract just analysis
3. **Inconsistent Format**: Each report has different analysis structure

---

## 3. Proposed Solution

### Decision: Separate Analysis Files

**New Structure:**
```
.autonomous/analysis/
├── reports/
│   └── scout-report-20260205.yaml      # Raw data only
├── analyses/
│   └── scout-report-20260205.analysis.yaml  # Analysis only
└── index.yaml                           # Analysis index
```

**Analysis Schema:**

```yaml
# scout-report-20260205.analysis.yaml
version: "1.0"
report_id: "scout-20260205"
analysis_id: "analysis-20260205"
timestamp: "2026-02-05T10:00:00Z"

summary:
  overall_assessment: "POSITIVE"
  confidence: 0.85
  key_findings_count: 3

key_findings:
  - id: "KF-001"
    category: "security"
    severity: "HIGH"
    finding_id: "F-001"  # Reference to report
    analysis: |
      The presence of hardcoded credentials in config.yaml
      represents a critical security vulnerability. This pattern
      suggests inadequate secrets management practices.
    implications:
      - "Credentials exposed in version control"
      - "Risk of unauthorized access"
    recommendations:
      - "Move credentials to environment variables"
      - "Implement secrets management solution"
      - "Rotate exposed credentials immediately"

trends:
  - category: "security"
    trend: "IMPROVING"
    evidence: "Fewer credential issues than last scan"

comparisons:
  vs_previous: "15% improvement in code quality"
  vs_baseline: "On track with quality goals"

metadata:
  analyst: "scout-intelligent"
  analysis_duration_seconds: 45
  confidence_factors:
    - "Multiple data points confirm finding"
    - "Pattern matches known vulnerability"
```

### Implementation Plan

#### Phase 1: Design Schema (1 hour)

Define analysis structure:
- Summary section
- Key findings with references
- Trends and comparisons
- Metadata

#### Phase 2: Create Extraction Script (2 hours)

**File:** `2-engine/.autonomous/bin/extract-analysis.py`

```python
#!/usr/bin/env python3
"""Extract analysis from reports into separate files."""

import yaml
from pathlib import Path

def extract_analysis(report_path: Path) -> dict:
    """Extract analysis section from a report."""
    with open(report_path) as f:
        report = yaml.safe_load(f)

    analysis = {
        'version': '1.0',
        'report_id': report['report_id'],
        'analysis_id': f"analysis-{report['report_id']}",
        'timestamp': report['timestamp'],
        'summary': {
            'overall_assessment': derive_assessment(report),
            'confidence': calculate_confidence(report),
            'key_findings_count': len(report.get('findings', []))
        },
        'key_findings': [],
        'trends': extract_trends(report),
        'comparisons': extract_comparisons(report),
        'metadata': {
            'analyst': report.get('agent', 'unknown'),
            'analysis_duration_seconds': report.get('duration_seconds', 0)
        }
    }

    # Extract key findings with references
    for finding in report.get('findings', []):
        analysis['key_findings'].append({
            'id': f"KF-{finding['id']}",
            'category': finding.get('category', 'unknown'),
            'severity': finding.get('severity', 'MEDIUM'),
            'finding_id': finding['id'],
            'analysis': finding.get('analysis', ''),
            'implications': finding.get('implications', []),
            'recommendations': [finding.get('recommendation', '')]
        })

    return analysis

def process_report(report_path: Path):
    """Process a single report."""
    analysis = extract_analysis(report_path)

    # Write analysis file
    output_path = report_path.parent.parent / 'analyses' / f"{report_path.stem}.analysis.yaml"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        yaml.dump(analysis, f, default_flow_style=False)

    print(f"Extracted analysis: {output_path}")
```

#### Phase 3: Run Extraction (1 hour)

1. Run extraction on all existing reports
2. Verify extracted analysis
3. Create analysis index

#### Phase 4: Update Report Generation (1 hour)

Update report generators to:
- Keep raw data in reports
- Generate separate analysis files
- Link between them

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/bin/extract-analysis.py` - Extraction script
2. `5-project-memory/blackbox5/.autonomous/analysis/analyses/` - Analysis directory

### Modified Files
1. Report generation scripts
2. Report reading scripts

---

## 5. Success Criteria

- [ ] Analysis schema defined
- [ ] Extraction script created
- [ ] All existing reports processed
- [ ] Analysis files created for all reports
- [ ] Report generation updated
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Keep analysis embedded in reports
2. **Fix**: Debug extraction script
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Schema | 1 hour | 1 hour |
| Phase 2: Extraction Script | 2 hours | 3 hours |
| Phase 3: Run Extraction | 1 hour | 4 hours |
| Phase 4: Update Generation | 1 hour | 5 hours |
| **Total** | | **4-5 hours** |

---

*Plan created based on SSOT violation analysis - Analysis embedded in reports*
