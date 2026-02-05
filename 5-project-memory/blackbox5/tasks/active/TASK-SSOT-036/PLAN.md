# PLAN.md: Standardize Report Formats

**Task:** TASK-SSOT-036 - Report formats inconsistent across agents
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Different agents produce reports in different formats:
- Scout: JSON or YAML, varying schemas
- Verifier: Custom format
- Executor: Different structure
- No standardization

This creates:
1. **Parsing Complexity**: Need multiple parsers
2. **Inconsistent Data**: Same concepts, different structures
3. **Aggregation Difficulty**: Hard to combine reports
4. **Maintenance Overhead**: Multiple format support

### First Principles Solution
- **Standard Schema**: Common report structure
- **Validation**: Ensure reports follow schema
- **Versioning**: Schema evolution support
- **Migration**: Convert existing reports

---

## 2. Proposed Solution

### Standard Report Schema

```yaml
version: "1.0"
report_id: "report-20260205-001"
report_type: "scout"  # scout, verifier, executor, etc.
timestamp: "2026-02-05T10:00:00Z"

metadata:
  agent: "scout-intelligent"
  agent_version: "1.0"
  task_id: "TASK-001"
  duration_seconds: 120
  input_summary: "Analyzed 150 files"

summary:
  status: "completed"  # completed, partial, failed
  overall_assessment: "POSITIVE"  # POSITIVE, NEGATIVE, MIXED
  key_metrics:
    files_processed: 150
    issues_found: 12
    recommendations: 5

findings:
  - id: "F-001"
    severity: "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: "security"
    title: "Hardcoded credentials found"
    description: "Credentials found in config.yaml"
    location:
      file: "config.yaml"
      line: 45
      column: 10
    evidence: "api_key: 'secret123'"
    recommendation: "Move to environment variables"
    references:
      - "https://owasp.org/credentials"

recommendations:
  - id: "R-001"
    priority: 1
    title: "Fix hardcoded credentials"
    description: "Move all credentials to env vars"
    effort: "2 hours"
    impact: "HIGH"
    related_findings: ["F-001"]

appendix:
  raw_data: {}  # Optional raw data
  logs: []      # Optional execution logs
```

### Implementation Plan

#### Phase 1: Define Schema (1 hour)

1. Create schema definition
2. Define validation rules
3. Create example reports

#### Phase 2: Create Validation (1 hour)

```python
import jsonschema

REPORT_SCHEMA = {
    "type": "object",
    "required": ["version", "report_id", "report_type", "timestamp"],
    "properties": {
        "version": {"type": "string"},
        "report_id": {"type": "string"},
        "report_type": {"enum": ["scout", "verifier", "executor", "planner"]},
        "timestamp": {"type": "string", "format": "date-time"},
        # ... more properties
    }
}

def validate_report(report: dict) -> bool:
    """Validate report against schema."""
    jsonschema.validate(report, REPORT_SCHEMA)
    return True
```

#### Phase 3: Update Agents (1 hour)

Update all agents to produce standard format:
- Scout
- Verifier
- Executor
- Planner

#### Phase 4: Migrate Existing Reports (1 hour)

Create migration script for old reports.

---

## 3. Success Criteria

- [ ] Standard schema defined
- [ ] Validation working
- [ ] All agents updated
- [ ] Old reports migrated

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Schema | 1 hour |
| Validation | 1 hour |
| Agents | 1 hour |
| Migration | 1 hour |
| **Total** | **3-4 hours** |

---

*Plan created based on SSOT violation analysis*
