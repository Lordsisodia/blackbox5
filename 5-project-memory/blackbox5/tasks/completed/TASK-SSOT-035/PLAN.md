# PLAN.md: Extract Analysis from Reports

**Task:** TASK-SSOT-035 - Analysis data embedded in report files
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 4-5 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Analysis is embedded in reports:
- Scout reports contain raw data + analysis
- Verifier reports contain tests + analysis
- No separation between data and interpretation

This creates:
1. **Extraction Difficulty**: Hard to get just analysis
2. **Mixed Concerns**: Data and analysis together
3. **No Aggregation**: Can't aggregate analysis across reports
4. **Duplication**: Same analysis patterns repeated

### First Principles Solution
- **Separation**: Analysis separate from raw data
- **Structured Format**: Standard analysis schema
- **Referential**: Analysis references source data
- **Aggregation**: Easy to combine analyses

---

## 2. Proposed Solution

### Separate Analysis Files

**Structure:**
```
.autonomous/analysis/
├── reports/
│   └── scout-report-20260205.yaml      # Raw data
├── analyses/
│   └── scout-report-20260205.analysis.yaml  # Analysis
└── index.yaml
```

**Analysis Schema:**
```yaml
analysis_id: "analysis-20260205"
report_id: "scout-20260205"
timestamp: "2026-02-05T10:00:00Z"

summary:
  overall_assessment: "POSITIVE"
  confidence: 0.85
  key_findings_count: 3

key_findings:
  - id: "KF-001"
    category: "security"
    severity: "HIGH"
    finding_id: "F-001"
    analysis: |
      Hardcoded credentials represent a critical
      security vulnerability indicating inadequate
      secrets management.
    implications:
      - "Credentials exposed in version control"
    recommendations:
      - "Move to environment variables"

trends:
  - category: "security"
    trend: "IMPROVING"
```

### Implementation Plan

#### Phase 1: Create Extraction Script (2 hours)

```python
def extract_analysis(report_path: Path) -> dict:
    """Extract analysis from report."""
    report = yaml.safe_load(report_path.read_text())

    analysis = {
        'analysis_id': f"analysis-{report['report_id']}",
        'report_id': report['report_id'],
        'timestamp': report['timestamp'],
        'summary': {
            'overall_assessment': derive_assessment(report),
            'key_findings_count': len(report.get('findings', []))
        },
        'key_findings': []
    }

    for finding in report.get('findings', []):
        analysis['key_findings'].append({
            'id': f"KF-{finding['id']}",
            'category': finding.get('category'),
            'severity': finding.get('severity'),
            'finding_id': finding['id'],
            'analysis': finding.get('analysis', ''),
            'recommendations': [finding.get('recommendation', '')]
        })

    return analysis
```

#### Phase 2: Run Extraction (1 hour)

Extract analysis from all existing reports.

#### Phase 3: Update Report Generation (1 hour)

Update report generators to create separate analysis files.

#### Phase 4: Create Analysis Index (1 hour)

Create searchable index of all analyses.

---

## 3. Success Criteria

- [ ] Extraction script created
- [ ] All reports processed
- [ ] Analysis files created
- [ ] Index created

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Script | 2 hours |
| Extraction | 1 hour |
| Report Generation | 1 hour |
| Index | 1 hour |
| **Total** | **4-5 hours** |

---

*Plan created based on SSOT violation analysis*
